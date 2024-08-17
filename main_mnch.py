import data_access.reader_population
import data_access.reader_on_off_track
import data_access.reader_sdmx

# Constants
# The data is hosted on a SDMX registry, it has convenient APIs to download data, use the query builder to craft the Query URL
DATA_URL_MNCH = "https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,GLOBAL_DATAFLOW,1.0/.MNCH_ANC4+MNCH_SAB.?format=sdmx-csv&labels=id"
# file paths for population data and on/off track data
FPATH_POPULATION = "01_rawdata/WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"
FPATH_ONOFF_TRACK = "01_rawdata/On-track and off-track countries.xlsx"

df_mnch = data_access.reader_sdmx.get_data_as_dataframe(DATA_URL_MNCH)
print(df_mnch.head())


df_pop = data_access.reader_population.get_data_as_dataframe(
    FPATH_POPULATION, sheet_name="Projections"
)
print(df_pop.head())


df_track = data_access.reader_on_off_track.get_data_as_dataframe(FPATH_ONOFF_TRACK)
print(df_track.head())

