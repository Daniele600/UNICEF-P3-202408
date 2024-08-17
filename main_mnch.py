import pandas as pd

import data_access.reader_population
import data_access.reader_on_off_track
import data_access.reader_sdmx

# Constants
# The data is hosted on a SDMX registry, it has convenient APIs to download data, use the query builder to craft the Query URL
DATA_URL_MNCH = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/.MNCH_ANC4+MNCH_SAB.?format=sdmx-csv&labels=id"
# file paths for population data and on/off track data
FPATH_POPULATION = "01_rawdata/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
FPATH_ONOFF_TRACK = "01_rawdata/On-track and off-track countries.xlsx"

"""Start data processing/cleaning section"""


def process_mnch(df: pd.DataFrame) -> pd.DataFrame:
    # A few checks before removing the unit multiplier, to avoid introducing errors if the multiplier changes in future releases
    unit_mult_unique = df["UNIT_MULTIPLIER"].unique()
    assert (
        len(unit_mult_unique) == 1 and unit_mult_unique[0] == 0
    ), "Unit Multiplier for MNCH is not 0 check and refine the script"
    assert (
        len(unit_mult_unique) == 1
    ), "Unit Multiplier for MNCH is not constant check and refine the script"
    assert len(df["AGE"].unique()) == 1, "Multiple age groups in MNCH dataset"

    # Drop non needed cols
    cols_to_remove = [
        "DATAFLOW",
        "SEX",
        "UNIT_MULTIPLIER",
        "OBS_CONF",
        "DATA_SOURCE",
        "SOURCE_LINK",
        "TIME_PERIOD_METHOD",
        "OBS_FOOTNOTE",
        "OBS_STATUS",
        "COVERAGE_TIME",
        "AGE",
        "WGTD_SAMPL_SIZE",
        "SERIES_FOOTNOTE",
        "CUSTODIAN",
        "REF_PERIOD",
        "LOWER_BOUND",
        "UPPER_BOUND",
    ]
    df = df.drop(columns=cols_to_remove)

    # We only consider data points between 2018 and 2022
    df = df[(df["TIME_PERIOD"] >= 2018) & (df["TIME_PERIOD"] <= 2022)]
    # Select the most recent year if there are multiple data points in the 2018 - 2022 time range
    df = df.sort_values(by=["TIME_PERIOD"]).drop_duplicates(
        subset=["REF_AREA", "INDICATOR"], keep="last"
    )
    # Sort again, just to keep the dataset ordered by area code
    df = df.sort_values(by=["REF_AREA"])
    # Rename the OBS_VALUE column to Coverage, it will be easier to handle when we merge with other data
    df = df.rename(columns={"OBS_VALUE": "COVERAGE"})

    # Express the percentage between 0 and 1
    df["COVERAGE"] = df["COVERAGE"] / 100

    return df


def process_population_data(df: pd.DataFrame) -> pd.DataFrame:
    # We're interested in country analysis, we can drop the rows having ISO3 Alpha-code empty as they're aggregates
    df = df.dropna(subset=["ISO3 Alpha-code"])
    # remove non needed columns (list the ones to keep and drop the rest)
    cols_to_keep = [
        "ISO3 Alpha-code",
        "Year",
        "Births (thousands)",
    ]
    cols_to_remove = [c for c in df.columns if c not in cols_to_keep]
    df = df.drop(columns=cols_to_remove)

    # only keep the 2022 projections
    df = df[df["Year"] == 2022]
    df = df.drop(columns=["Year"])

    # Apply the multiplier
    df["Births (thousands)"] = df["Births (thousands)"] * 1000

    # column names harmonization
    cols_rename = {
        "ISO3 Alpha-code": "REF_AREA",
        "Births (thousands)": "DM_BIRTHS",
    }
    df = df.rename(columns=cols_rename)

    return df


def process_on_off_track_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["OfficialName"])

    # column names harmonization
    cols_rename = {"ISO3Code": "REF_AREA", "Status.U5MR": "STATUS_U5MR"}
    df = df.rename(columns=cols_rename)

    return df


"""End data processing/cleaning section"""


"""Read and process data start"""
df_mnch = data_access.reader_sdmx.get_data_as_dataframe(DATA_URL_MNCH)
df_mnch = process_mnch(df_mnch)

df_pop = data_access.reader_population.get_data_as_dataframe(
    FPATH_POPULATION, sheet_name="Projections"
)
df_pop = process_population_data(df_pop)

df_track = data_access.reader_on_off_track.get_data_as_dataframe(FPATH_ONOFF_TRACK)
df_track = process_on_off_track_data(df_track)
"""Read and process data end"""

"""Merge data start"""
# Drop the countries that are not in the on_track off_track dataset
df_mnch = df_mnch[df_mnch["REF_AREA"].isin(df_track["REF_AREA"].unique())]
# Merge on track off track data with population data
df = df_track.merge(df_pop, left_on=["REF_AREA"], right_on=["REF_AREA"], how="left")
assert len(df) == len(
    df_track
), "The join of df_track and df_pop generated unwanted rows, check"
del df_pop

df = df_mnch.merge(
    df,
    left_on=["REF_AREA"],
    right_on=["REF_AREA"],
    how="left",
)
assert len(df) == len(
    df_mnch
), "The join of df and df_mnch generated unwanted rows, check"
del df_mnch
"""Merge data end"""


# Start the analysys and chart
def calc_weighted_coverage(df: pd.DataFrame) -> float:
    """ """
    ret = (df["COVERAGE"] * df["DM_BIRTHS"]).sum() / (df["DM_BIRTHS"].sum())
    ret = ret * 100.0
    return ret


# We're only interested in the On track and Acceleration needed rows, remove the rows with status == achieved
df = df[df["STATUS_U5MR"] != "Achieved"]

# Split in 2 dataframes: ANC4 abd SAB
df_anc4 = df[df["INDICATOR"] == "MNCH_ANC4"]
df_sab = df[df["INDICATOR"] == "MNCH_SAB"]

#Calculate the weighted values
weighted_ANC4_ontrack = calc_weighted_coverage(
    df_anc4[df_anc4["STATUS_U5MR"] == "On Track"]
)
weighted_ANC4_offtrack = calc_weighted_coverage(
    df_anc4[df_anc4["STATUS_U5MR"] == "Acceleration Needed"]
)
weighted_SAB_ontrack = calc_weighted_coverage(
    df_sab[df_sab["STATUS_U5MR"] == "On Track"]
)
weighted_SAB_offtrack = calc_weighted_coverage(
    df_sab[df_sab["STATUS_U5MR"] == "Acceleration Needed"]
)

