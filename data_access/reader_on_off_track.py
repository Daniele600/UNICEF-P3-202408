import pandas as pd


def get_data_as_dataframe(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    return df
