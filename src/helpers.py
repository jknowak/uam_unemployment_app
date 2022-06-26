"""
This is a module containing useful function for transforming
the data that feeds the dash app
"""
from datetime import date
import pandas as pd


months_dict = {
    "styczeń": 1,
    "luty": 2,
    "marzec": 3,
    "kwiecień": 4,
    "maj": 5,
    "czerwiec": 6,
    "lipiec": 7,
    "sierpień": 8,
    "wrzesień": 9,
    "październik": 10,
    "listopad": 11,
    "grudzień": 12,
}


def filter_year_gender(df_input: pd.DataFrame, year: list, gender: str) -> pd.DataFrame:
    """
    Allows to filter a dataframe by year or gender
    :param df_input:
    :param year:
    :param gender:
    :return:
    """
    if year is None:
        year = (min(df_input.Rok), max(df_input.Rok))
    if gender is None:
        gender = df_input.Płeć.unique()
    tmp = df_input.loc[df_input.loc[:, "Płeć"].isin(gender), :]  # pylint: disable=E1101
    tmp = tmp[tmp.loc[:, "Rok"] <= year[1]]
    tmp = tmp[tmp.loc[:, "Rok"] >= year[0]]
    return tmp


def load_raw_data(path: str) -> pd.DataFrame:
    """
    Loads a semicolon separated DataFrame from a path
    :param path:
    :return:
    """
    with open(
        path,
        encoding="utf8",
        errors="ignore",
    ) as open_file:
        return pd.read_csv(open_file, sep=";")


def add_proper_date(df_: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a date column to a DataFrame based on Year and Months columns
    :param df_:
    :return:
    """
    df_["Data"] = df_.apply(
        lambda x: date(x["Rok"], months_dict.get(x["Miesiące"]), 1), axis=1
    )
    return df_
