import pandas as pd
from dateutil.relativedelta import relativedelta

import data_access.edu_export

# Constants
INPUT_FILE_PATH = file_path = "01_rawdata/Zimbabwe_children_under5_interview.csv"
OUT_FILE_PATH = "outputs_edu/edu_data.js"

# keep a list of the categorical columns containing y/n (EC6 -> EC15)
categorical_cols = [f"EC{i}" for i in range(6, 16)]

# Defining the dataframe's data type to ensure correct calculations
data_dtypes = {
    "interview_date": str,
    "child_age_years": int,
    "child_birthday": str,
}
for c in categorical_cols:
    data_dtypes[c] = "category"

# A map for the categories, using y,n,dk,other to have a better visual understanding of the data
categories_map = {"1": "y", "2": "n", "8": "dk", "9": "other"}
# Map the indicators' codes to a label
indicators_title_map = {
    "EC6": "Can identify or name at least ten letters of the alphabet",
    "EC7": "Can read at least four simple, popular words",
    "EC8": "Does know the name and recognize the symbol of all numbers from 1 to 10",
    "EC9": "Can pick up a small object with two fingers, like a stick or a rock from the ground",
    "EC10": "Is sometimes too sick to play",
    "EC11": "Does follow simple directions on how to do something correctly",
    "EC12": "When given something to do, is able to do it independently",
    "EC13": "Does get along well with other children",
    "EC14": "Does kick, bite, or hit other children or adults",
    "EC15": "Does get distracted easily",
}

"""util functions"""


# Calculate the diffence in months from the 3 years (e.g. exaclty 3 years old would be 0 months)
def months_diff(start_date, end_date):
    delta = relativedelta(end_date, start_date)
    return (delta.years - 3) * 12 + delta.months


def count_categories_by_month(df: pd.DataFrame, category_columns: list) -> pd.DataFrame:
    """Takes a dataframe with a MONTH and n categorical columns
    The MONTH column contains how many months have passed since the 3 years birthday and before the 5th (0->23)
    The categories contain 1,2,8,9 values

    The function creates a Dataframe with columns: MONTHS, CATEGORY, COUNT, INDICATOR
    MONTHS: the age since 3 years in months
    CATEGORY: The category of the answer (1:yes, 2:no, 8:DK, 9:?)
    COUNT: How many answers of that particular category we gathered in the surveys
    INDICATOR: The id of the question

    E.g. an example row is:
     MONTHS: 1 (The children are 3 years and 1 month old)
     CATEGORY: 1 (Answer = Yes)
     COUNT: 92 (we gathered 92 yes answers)
     INDICATOR: EC6 (the question is EC6)

    Args:
        df (pd.Dataframe): The dataframe containing the data

    Returns:
        pd.DataFrame: A pandas dataframe containing results by category
    """
    df_ret = pd.DataFrame()
    for col in category_columns:
        tmp = (
            df.groupby(["MONTHS", col], observed=True).size().reset_index(name="COUNT")
        )
        tmp["INDICATOR"] = col
        tmp = tmp.rename(columns={col: "CATEGORY"})
        df_ret = pd.concat([df_ret, tmp], ignore_index=True)
    return df_ret


"""Start reading and cleaning"""
# read the data
df = pd.read_csv(file_path, dtype=data_dtypes)

# Drop the rows without child_birthday -> we cannot calculate the exact age of the child
df = df.dropna(subset=["child_birthday"])

# Convert dates columns to date types
df["interview_date"] = pd.to_datetime(df["interview_date"], format="%Y-%m-%d")
df["child_birthday"] = pd.to_datetime(df["child_birthday"], format="%Y-%m-%d")

# create the "MONTHS" column, it contains how many months have passed since the child's three years
df["MONTHS"] = df.apply(
    lambda row: months_diff(row["child_birthday"], row["interview_date"]), axis=1
)
# We don't need the interview_date and child_birthday columns anymore
df = df.drop(columns=["interview_date", "child_birthday"])

df_monthly_trends = count_categories_by_month(df, categorical_cols)
# map the numeric categories with strings, are easier to look at
df_monthly_trends = df_monthly_trends.replace({"CATEGORY": categories_map})
# Remove the DK and Other categories (would need further investigation to understand if they're "hiding" useful information)
df_monthly_trends = df_monthly_trends[df_monthly_trends["CATEGORY"].isin(["y", "n"])]
# pivot the table, passing from columns:
# MONTHS CATEGORY  COUNT INDICATOR
# to columns:
# MONTHS INDICATOR n y
df_ratios = df_monthly_trends.pivot_table(
    index=["MONTHS", "INDICATOR"], columns="CATEGORY", values="COUNT"
)
df_ratios = df_ratios.reset_index()
# Calculate the percentage of yes answers on the total answers and round
df_ratios["pcnt"] = (df_ratios["y"] / (df_ratios["y"] + df_ratios["n"])) * 100
df_ratios["pcnt"] = round(df_ratios["pcnt"], 1)

# we generated the data, we now want to create a visualization in HTML, pass the data to the exporter function
data_access.edu_export.export(
    OUT_FILE_PATH, df_ratios, categorical_cols, indicators_title_map
)
