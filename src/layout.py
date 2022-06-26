"""
A module creating the content layout of the main app
"""

import time
from datetime import date
from typing import Any

from dateutil.relativedelta import relativedelta
import plotly.express as px  # type: ignore

# import pandas as pd  # type: ignore
from dash import html, dcc, dash_table  # type: ignore
from dash.dependencies import Input, Output  # type: ignore

from maindash import app
from data_pipeline import prep_data

df, df2 = prep_data()


def make_layout() -> html.Div:
    """
    Creates the layout of the dashboard
    :return: A Html div containing all elements
    """
    return html.Div(
        children=[
            html.H1(
                children="Bezrobocie w Polsce przed pandemią i po pandemii COVID-19"
            ),
            html.Div(
                children="""
            Aplikacja napisana w Dashu
        """
            ),
            # chart 1
            # date slider
            html.Div(
                [
                    html.H3(children="Miesiąc", className="card"),
                    dcc.DatePickerRange(
                        id="month-selection",
                        min_date_allowed=date(2017, 1, 1),
                        max_date_allowed=date(2021, 12, 1),
                        initial_visible_month=date(2017, 1, 1),
                        display_format="YYYY-MM",
                        start_date=date(2017, 1, 1),
                        end_date=date(2021, 12, 1),
                    ),
                ]
            ),
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
            html.Div(dcc.Graph(id="chart_plc_mo_rel")),
            html.Br(),
            # dropdown wojewodztwo
            html.Div(
                [
                    html.H3(children="Województwo", className="card"),
                    dcc.Dropdown(
                        df[
                            df.Nazwa != "POLSKA"
                        ].Nazwa.unique(),  # pylint: disable=E1101, E1136
                        df[
                            df.Nazwa != "POLSKA"
                        ].Nazwa.unique(),  # pylint: disable=E1101, E1136
                        id="voivodship-selection",
                        multi=True,
                    ),
                ]
            ),
            html.Div(dcc.Graph(id="chart_woj_mo")),
            html.Div(dcc.Graph(id="chart_woj_mo_rel")),
            # html.Div(dash_table.DataTable(id="tbl")),
            # chart 2
            html.H5(children="Bezrobocie w Polsce dla danych lat i płci"),
            html.Div(
                [
                    dash_table.DataTable(
                        id="data_table",
                        columns=[{"name": col, "id": col} for col in df2.columns],
                        editable=True,
                        # filter_action='native',
                        sort_action="native",
                        page_action="native",
                        page_current=0,
                        page_size=20,
                        column_selectable="multi",
                        # row_selectable='multi',
                        # row_deletable=True
                    )
                ]
            )
            # chart 3
            # chart 4
            # chart 5
        ],
        style={"padding": "20px 20px 20px 20px"},
    )


# decorator that enables reactivity
@app.callback(
    [Output("chart_plc_mo", "figure"), Output("chart_plc_mo_rel", "figure")],
    [
        Input("gender-selection", "value"),
        Input("month-selection", "start_date"),
        Input("month-selection", "end_date"),
    ],
)
def update_graph_plc(
    selected_gender_value: str, month_selection_start: str, month_selection_end: str
) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_gender_value:
    :param month_selection_start:
    :param month_selection_end:
    :return: two updated plotly figures
    """
    ms_ = date.fromisoformat(month_selection_start)
    me_ = date.fromisoformat(month_selection_end)
    tmp = df.loc[  # pylint: disable=E1101
        df.loc[:, "Płeć"].isin(selected_gender_value), :  # pylint: disable=E1101
    ]
    tmp = tmp[tmp.loc[:, "Data"] <= me_]
    tmp = tmp[tmp.loc[:, "Data"] >= ms_]
    tmp = tmp.groupby(["Data", "Płeć"]).agg({"Wartosc": sum}).reset_index()
    tmp["Wartosc_rel"] = tmp.apply(
        lambda x: x.Wartosc
        / int(tmp[(tmp.Płeć == x.Płeć) & (tmp.Data == tmp.Data.min())]["Wartosc"])
        * 100,
        axis=1,
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
    if ms_.day > 1:
        ms_ = ms_ + relativedelta(months=1)
    fig.update_layout(barmode="overlay")
    fig_rel = px.line(
        tmp,
        x="Data",
        y="Wartosc_rel",
        color="Płeć",
        title=f"Bezrobocie według płci - wartość w stosunku do {ms_.year}-{ms_.month}",
        labels={
            "Data": "Data",
            "Wartosc_rel": f"Relatywna l. bezrobotnych (100 = {ms_.year}-{ms_.month})",
        },
    )
    fig.update_layout(barmode="overlay")
    return fig, fig_rel


@app.callback(
    [Output("chart_woj_mo", "figure"), Output("chart_woj_mo_rel", "figure")],
    [
        Input("voivodship-selection", "value"),
        Input("month-selection", "start_date"),
        Input("month-selection", "end_date"),
    ],
)
def update_graph_voi(
    selected_voivod_value: str, month_selection_start: str, month_selection_end: str
) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_voivod_value:
    :param month_selection_start:
    :param month_selection_end:
    :return: two updated plotly figures
    """
    ms_ = date.fromisoformat(month_selection_start)
    me_ = date.fromisoformat(month_selection_end)
    tmp = df.loc[  # pylint: disable=E1101
        df.loc[:, "Nazwa"].isin(selected_voivod_value), :  # pylint: disable=E1101
    ]
    tmp = tmp[tmp.loc[:, "Data"] <= me_]
    tmp = tmp[tmp.loc[:, "Data"] >= ms_]
    tmp = tmp.groupby(["Data", "Nazwa"]).agg({"Wartosc": sum}).reset_index()
    tmp["Wartosc_rel"] = tmp.apply(
        lambda x: x.Wartosc
        / int(tmp[(tmp.Nazwa == x.Nazwa) & (tmp.Data == tmp.Data.min())]["Wartosc"])
        * 100,
        axis=1,
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
    if ms_.day > 1:
        ms_ = ms_ + relativedelta(months=1)
    fig.update_layout(barmode="overlay")
    fig_rel = px.line(
        tmp,
        x="Data",
        y="Wartosc_rel",
        color="Nazwa",
        title=f"Bezrobocie według województwa - wartość w stosunku do {ms_.year}-{ms_.month}",
        labels={
            "Data": "Data",
            "Wartosc_rel": f"Relatywna l. bezrobotnych (100 = {ms_.year}-{ms_.month})",
        },
    )
    fig_rel.update_layout(barmode="overlay")
    return fig, fig_rel


@app.callback(
    Output("data_table", "data"),
    [
        Input("gender-selection", "value"),
        Input("month-selection", "start_date"),
        Input("month-selection", "end_date"),
    ],
)
def update_table(
    selected_gender_value: str, month_selection_start: str, month_selection_end: str
) -> Any:
    """
    Updates the plot according to the selected values

    :param selected_gender_value:
    :param month_selection_start:
    :param month_selection_end:
    :return: two updated plotly figures
    """
    tmp = df2.loc[  # pylint: disable=E1101
        df2.loc[:, "Płeć"].isin(selected_gender_value), :  # pylint: disable=E1101
    ]
    tmp = tmp[tmp.loc[:, "Rok"] <= date.fromisoformat(month_selection_end).year]
    tmp = tmp[tmp.loc[:, "Rok"] >= date.fromisoformat(month_selection_start).year]

    # "dlugie obliczenia"
    time.sleep(3)

    return tmp.to_dict("records")
