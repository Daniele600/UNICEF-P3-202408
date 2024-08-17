import pandas as pd
import requests
import json


def get_data_as_dataframe(url: str) -> pd.DataFrame:
    """Given the complete URL (API endpoint + parameters) returns the data as a dataframe. The url is passed "as is" to allow flexibility, URL can be changed as long as it returns a CSV file

    Args:
        url (str): The complete URL, can be created using the Query builder

    Returns:
        pd.DataFrame: A pandas dataframe containing the data
    """

    # Reading the csv directly from Pandas, we're using an SDMX registry, the registry's default encoding is UTF8, add it as param just to be on the safe side
    df = pd.read_csv(url, encoding="utf-8")
    # return the pandas dataframe
    return df
