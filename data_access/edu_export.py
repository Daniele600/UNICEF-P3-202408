import pandas as pd
import json
import os


def export(out_filepath: str, df: pd.DataFrame, indicators: list, indic_titles: dict):
    """Creates and save a js file that will be used by the visualization interface


    Args:
        filepath (string): The output file
        df (pd.Dataframe): The dataframe containing the data
        indicators: The lsit of indicators
        indic_titles: The lsit of indicators' titles

    Returns:
        pd.DataFrame: A pandas dataframe containing results by category
    """
    to_save = []
    for ind in indicators:
        df_tmp = df[df["INDICATOR"] == ind]
        df_tmp = df_tmp.sort_values(by=["MONTHS"])

        # the objects to add to the json
        to_add = {
            "id": ind,
            "title": indic_titles[ind],
            "x": [],
            "y": [],
        }

        for idx, row in df_tmp.iterrows():
            y = 3
            if row["MONTHS"] > 11:
                y = 4
            to_add["x"].append(f"{y} Years, {row['MONTHS']} months")
            to_add["y"].append(f'{row["pcnt"]}')

            explaination_filepath = f"{ind}.txt"
            explaination = ""
        if os.path.isfile(explaination_filepath):
            with open(explaination_filepath, "r") as file:
                explaination = file.read()
        else:
            print(explaination_filepath + " not found")
        to_add["explaination"] = explaination

        to_save.append(to_add)

    json_string = json.dumps(to_save)
    json_string = "var edu_data = " + json_string
    with open(out_filepath, "w") as text_file:
        text_file.write(json_string)
