"""
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.

Każda akcja powoduje konieczność ,,kosztownego przeliczenia" trwającego 3 sekundy.

"""

import time
from typing import Any
import plotly.express as px  # type: ignore
import pandas as pd  # type: ignore
from dash import Dash, html, dcc, dash_table  # type: ignore
from dash.dependencies import Input, Output  # type: ignore


app = Dash(__name__, assets_folder="../assets")

# źródło danych
# https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
# https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
with open(
    "data/raw_data/bezrobocie_plec_miesiecznie.csv",
    encoding="utf8",
    errors="ignore",
) as f:
    df: pd.DataFrame = pd.read_csv(f, sep=";")
'''
with open(
    "data/raw_data/bezrobocie_wyksz_plec_lata.csv",
    encoding="utf8",
    errors="ignore",
) as f:
    df2: pd.DataFrame = pd.read_csv(f, sep=";")
'''
# App layout
app.layout = html.Div(
    children=[
        html.H1(children="Bezrobocie w Polsce przed pandemią i po pandemii COVID-19"),
        html.Div(
            children="""
        Aplikacja napisana w Dashu
    """
        ),
        # dropdown
        html.Div(
            [
                html.H3(children="Płeć", className="card"),
                dcc.Dropdown(
                    df["Płeć"].unique(),
                    df["Płeć"].unique(),
                    id="gender-selection",
                    multi=True,
                ),
            ]
        ),
        html.Br(),
        # slider
        html.Div(
            [
                html.H3(children="Płeć", className="card"),
                dcc.Dropdown(
                    df["Miesiące"].unique(),
                    df["Miesiące"].unique(),
                    id="month-selection",
                    multi=True,
                ),
            ]
        ),
        html.Div(dcc.Graph(id="chart")),
        html.Div(dash_table.DataTable(id="tbl")),
    ]
)


# decorator that enables reactivity
@app.callback(
    [Output("chart", "figure"), Output("tbl", "data")],
    [Input("gender-selection", "value"), Input("month-selection", "value")],
)
def update_graph(selected_gender_value: str, month_selection_value: str) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_gender_value:
    :param month_selection_value:
    :return: updated plotly figure
    """
    tmp = df.loc[  # pylint: disable=E1101
        df.loc[:, "Płeć"].isin(selected_gender_value), :  # pylint: disable=E1101
    ]
    tmp = df.loc[  # pylint: disable=E1101
          df.loc[:, "Miesiące"].isin(month_selection_value), :  # pylint: disable=E1101
          ]
    tmp = (
        tmp.groupby("Miesiące")
        .agg({"Wartosc": sum})
        .reset_index()
    )
    # "dlugie obliczenia"
    time.sleep(3)

    fig = px.bar(
        tmp,
        x="Miesiące",
        y="Wartosc",
        color="Miesiące",
        title="Bezrobocie według wykształcenia",
        labels={
            "Miesiące": "Miesiące",
            "Wartosc": "Liczba bezrobotnych",
        },
    )

    fig.update_layout(barmode="overlay")

    return fig, tmp.to_dict("rows")


if __name__ == "__main__":
    app.run_server(debug=True)
