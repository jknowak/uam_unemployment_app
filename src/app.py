"""
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.

Każda akcja powoduje konieczność ,,kosztownego przeliczenia" trwającego 3 sekundy.

"""

import time
from datetime import date
from typing import Any
import plotly.express as px  # type: ignore
import pandas as pd  # type: ignore
from dash import Dash, html, dcc, dash_table  # type: ignore
from dash.dependencies import Input, Output  # type: ignore


app = Dash(__name__, assets_folder="../assets")

months_dict = {'styczeń': 1, 'luty': 2, 'marzec': 3,
               'kwiecień': 4, 'maj': 5, 'czerwiec': 6,
               'lipiec': 7,'sierpień': 8,'wrzesień': 9,
               'październik': 10, 'listopad': 11, 'grudzień': 12}
# źródło danych
# https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
# https://bdl.stat.gov.pl/bdl/dane/podgrup/wymiary
with open(
    "data/raw_data/bezrobocie_plec_miesiecznie.csv",
    encoding="utf8",
    errors="ignore",
) as f:
    df: pd.DataFrame = pd.read_csv(f, sep=";")
    df['Data'] = df.apply(lambda x: date(x['Rok'], months_dict.get(x['Miesiące']), 1), axis=1)
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
        # chart 1
        # date slider
        html.Div([
            html.H3(children="Miesiąc", className="card"),
            dcc.DatePickerRange(
                id='month-selection',
                min_date_allowed=date(2017, 1, 1),
                max_date_allowed=date(2021, 12, 1),
                initial_visible_month=date(2017, 1, 1),
                display_format='YYYY-MM',
                start_date=date(2017, 1, 1),
                end_date=date(2021, 12, 1)
            )
        ]),
        html.Br(),
        # dropdown plec
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
        html.Div(dcc.Graph(id="chart_plc_mo")),
        html.Br(),
        # dropdown wojewodztwo
        html.Div(
            [
                html.H3(children="Województwo", className="card"),
                dcc.Dropdown(
                    df[df.Nazwa != 'POLSKA']["Nazwa"].unique(),
                    df[df.Nazwa != 'POLSKA']["Nazwa"].unique(),
                    id="voivodship-selection",
                    multi=True,
                ),
            ]
        ),
        html.Div(dcc.Graph(id="chart_woj_mo")),
        #html.Div(dash_table.DataTable(id="tbl")),

        # chart 2

        # chart 3

        # chart 4

        # chart 5

    ], style={'padding': '20px 20px 20px 20px'})


# decorator that enables reactivity
@app.callback(
    Output("chart_plc_mo", "figure"),
    [Input("gender-selection", "value"), Input("month-selection", "start_date"), Input("month-selection", "end_date")],
)
def update_graph_plc(selected_gender_value: str, month_selection_start: str, month_selection_end: str) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_gender_value:
    :param month_selection_value:
    :return: updated plotly figure
    """
    tmp = df.loc[  # pylint: disable=E1101
        df.loc[:, "Płeć"].isin(selected_gender_value), :  # pylint: disable=E1101
    ]
    tmp = tmp[tmp.loc[:, "Data"] <= date.fromisoformat(month_selection_end)]
    tmp = tmp[tmp.loc[:, "Data"] >= date.fromisoformat(month_selection_start)]
    tmp = (
        tmp.groupby(["Data", "Płeć"])
        .agg({"Wartosc": sum})
        .reset_index()
    )
    # "dlugie obliczenia"
    time.sleep(3)

    fig = px.line(
        tmp,
        x="Data",
        y="Wartosc",
        color="Płeć",
        title="Bezrobocie według płci",
        labels={
            "Data": "Data",
            "Wartosc": "Liczba bezrobotnych",
        },
    )
    fig.update_layout(barmode="overlay")
    return fig


@app.callback(
    Output("chart_woj_mo", "figure"),
    [Input("voivodship-selection", "value"), Input("month-selection", "start_date"), Input("month-selection", "end_date")],
)
def update_graph_plc(selected_voivod_value: str, month_selection_start: str, month_selection_end: str) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_voivod_value:
    :param month_selection_value:
    :return: updated plotly figure
    """
    tmp = df.loc[  # pylint: disable=E1101
        df.loc[:, "Nazwa"].isin(selected_voivod_value), :  # pylint: disable=E1101
    ]
    tmp = tmp[tmp.loc[:, "Data"] <= date.fromisoformat(month_selection_end)]
    tmp = tmp[tmp.loc[:, "Data"] >= date.fromisoformat(month_selection_start)]
    tmp = (
        tmp.groupby(["Data", "Nazwa"])
        .agg({"Wartosc": sum})
        .reset_index()
    )
    # "dlugie obliczenia"
    time.sleep(3)

    fig = px.line(
        tmp,
        x="Data",
        y="Wartosc",
        color="Nazwa",
        title="Bezrobocie według województwa",
        labels={
            "Data": "Data",
            "Wartosc": "Liczba bezrobotnych",
        },
    )
    fig.update_layout(barmode="overlay")
    return fig



if __name__ == "__main__":
    app.run_server(debug=True)
