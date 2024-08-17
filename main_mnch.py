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

'''Start data processing/cleaning section'''
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

def process_population_data(df:pd.DataFrame) -> pd.DataFrame:
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
    # Convert years from floats to ints
    df["Year"] = df["Year"].astype(int)

    #Apply the multiplier
    df["Births (thousands)"] = df["Births (thousands)"] * 1000

    # column names harmonization
    cols_rename = {
        "ISO3 Alpha-code": "REF_AREA",
        "Year": "TIME_PERIOD",
        "Births (thousands)": "DM_BIRTHS",
    }
    df = df.rename(columns=cols_rename)

    return df

def process_on_off_track_data(df:pd.DataFrame) -> pd.DataFrame:
    df = df.drop(columns=["OfficialName"])

    # column names harmonization
    cols_rename = {"ISO3Code": "REF_AREA", "Status.U5MR": "STATUS_U5MR"}
    df = df.rename(columns=cols_rename)

    return df

'''End data processing/cleaning section'''


df_mnch = data_access.reader_sdmx.get_data_as_dataframe(DATA_URL_MNCH)
df_mnch = process_mnch(df_mnch)
print(df_mnch.head())


df_pop = data_access.reader_population.get_data_as_dataframe(
    FPATH_POPULATION, sheet_name="Projections"
)
df_pop = process_population_data(df_pop)
print(df_pop.head())


df_track = data_access.reader_on_off_track.get_data_as_dataframe(FPATH_ONOFF_TRACK)
df_track = process_on_off_track_data(df_track)
print(df_track.head())
