"""
Loads and prepares two data sources
"""
from typing import Tuple
import pandas as pd
from helpers import load_raw_data, add_proper_date


FILE1 = "bezrobocie_plec_miesiecznie.csv"
FILE2 = "bezrobocie_wyksz_plec_lata.csv"


def prep_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetches and processes two tables from csvs.
    :
    """
    # źródło danych
    # https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
    # https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
    df_ = load_raw_data(f"data/raw_data/{FILE1}")
    df_ = add_proper_date(df_)

    df_2 = load_raw_data(f"data/raw_data/{FILE2}")
    df_2 = df_2.loc[
        (df_2["Poziomy wykształcenia"] == "ogółem") & (df_2.Nazwa == "POLSKA"),
        ["Płeć", "Rok", "Wartosc"],
    ]

    return df_, df_2
