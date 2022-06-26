"""
Getting data for unit tests

"""
import pytest  # type: ignore
import pandas as pd  # type: ignore


@pytest.fixture(scope="session")
def example_data():
    """

    :return:
    """
    with open(
        "data/raw_data/bezrobocie_plec_miesiecznie.csv",
        encoding="utf8",
        errors="ignore",
    ) as file:
        df = pd.read_csv(file, sep=";")
    return df
