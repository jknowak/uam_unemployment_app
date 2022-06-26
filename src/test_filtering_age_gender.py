"""
Testing simple filtering function

"""
from app import filter_year_gender


def test_male_data(example_data):  # pylint: disable=W0621
    """

    :param example_data:
    :return:
    """
    df_x = filter_year_gender(example_data, year=None, gender=["mężczyźni"])

    assert len(df_x["Płeć"].unique()) == 1


def test_year_data(example_data):  # pylint: disable=W0621
    """

    :param example_data:
    :return:
    """
    df_x = filter_year_gender(example_data, year=[2017, 2020], gender=None)

    assert len(df_x["Rok"].unique()) <= 3
