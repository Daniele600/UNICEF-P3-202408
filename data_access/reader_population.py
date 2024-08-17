import pandas as pd


def get_data_as_dataframe(
    file_path: str, sheet_name: str = "Projections"
) -> pd.DataFrame:
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=16)
    return df
