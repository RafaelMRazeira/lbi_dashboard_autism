import numpy as np
import pandas as pd
from dash import html, dcc
import plotly.express as px
from lbi_dashboard_autism.data import DF_PLOT
from lbi_dashboard_autism.const import ALL_CITIES_SP, CITIES_SP_GEOJSON


FILTER_LAWSUITS_AMOUNT_BY_CITY = html.Div(
    [
        html.Div(
            [
                html.Label(
                    "FILTRAR POR CIDADE",
                    style={
                        "marginBottom": "5px",
                        "fontSize": "12px",
                    },
                ),
                dcc.Dropdown(
                    ALL_CITIES_SP,
                    multi=True,
                    clearable=True,
                    id="filter-city",
                ),
            ],
            style={
                "display": "flex",
                "flexDirection": "column",
                "width": "100%",
                "marginRight": "20px",
            },
        ),
    ],
    style={
        "display": "flex",
        "flexDirection": "row",
    },
)


def _lateral_card(title, most_id, amount_id, subtitle="dos processos",):
    return html.Div(
        [
            html.H6(
                children=title,
                style={
                    "textAlign": "center",
                    "color": "#252423",
                    "marginBottom": "3px",
                    "fontWeight": "400",
                    "fontSize": "14px",
                },
            ),
            html.P(
                None,
                style={
                    "textAlign": "center",
                    "color": "#118DFF",
                    "fontSize": "15px",
                    "fontWeight": "bold",
                    "marginTop": "5px",
                    "marginBottom": "15px",
                },
                id=most_id,
            ),
            html.P(
                None,
                style={
                    "textAlign": "center",
                    "color": "#252423",
                    "fontSize": "35px",
                    "margin": "0px",
                },
                id=amount_id,
            ),
            html.P(
                subtitle,
                style={
                    "textAlign": "center",
                    "color": "#252423",
                    "fontSize": 12,
                    "marginTop": "5px",
                    "marginLeft": "48px",
                    "fontWeight": "bold",
                },
            ),
        ],
        style={
            "backgroundColor": "#fff",
            "borderRadius": "15px",
            "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
            "margin": "0.25rem .25em",
        },
    )


TAB_VISAO_GERAL_PAGE = html.Div(
    [
        html.Div(
            [
                FILTER_LAWSUITS_AMOUNT_BY_CITY,
                html.Div(
                    [
                        html.H4(
                            children="Quantidade de Processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "marginBottom": "5px",
                                "fontWeight": "normal",
                                "fontSize": "13px",
                            },
                        ),
                        html.Div(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontWeight": "bold",
                                "fontSize": "32px",
                            },
                            id="total_cases",
                        ),
                    ],
                    style={},
                ),
                html.Div([html.Div(dcc.Graph(id="choropleth-map-amount"))], style={}),
            ],
            style={
                "backgroundColor": "#fff",
                "borderRadius": "15px",
                "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                "padding": "10px",
            },
        ),
        html.Div(
            [
                html.Div(
                    _lateral_card(
                        "Tempo médio de duração dos processos",
                        "total_time",
                        "total_time",
                        subtitle="dias",
                    ),
                    style={},
                ),
                html.Div(
                    [
                        _lateral_card(
                            "Assunto do Direito mais presente",
                            "most_subject",
                            "amount_most_subject",
                        ),
                        _lateral_card(
                            "Classe do Direito mais presente",
                            "most_class",
                            "amount_most_class",
                        ),
                        _lateral_card(
                            "Tipo do Direito mais presente",
                            "most_type",
                            "amount_most_type",
                        ),
                        _lateral_card(
                            "Vara do Direito mais presente",
                            "most_court",
                            "amount_most_court",
                        ),
                        _lateral_card(
                            "Juíz(a) mais presente", "most_judge", "amount_most_judge"
                        ),
                        _lateral_card(
                            "Escrivã(o) mais presente",
                            "most_clerk",
                            "amount_most_clerk",
                        ),
                    ],
                    style={
                        "display": "grid",
                        "gridTemplateColumns": "1fr 1fr",
                        "gridTemplateRows": "1fr 1fr 1fr",
                        "flexWrap": "wrap",
                    },
                ),
            ],
            style={},
        ),
    ],
    style={
        "display": "grid",
        "justifyContent": "space-between",
        "gridTemplateColumns": "1fr 1fr",
        "gap": "0.25em",
        "padding": "0.25em",
        "fontFamily": "Open Sans, sans-serif",
    },
)


def _filter_df(value_city):
    if value_city is None or value_city == []:
        return DF_PLOT
    return DF_PLOT.loc[DF_PLOT["city"].isin(value_city)]


def update_map_visao_geral(value_city):
    df_plot = _filter_df(value_city)

    fig = px.choropleth_mapbox(
        df_plot,
        geojson=CITIES_SP_GEOJSON,
        locations="city",
        color="Quantidade de Processos",
        color_continuous_scale=["#a9ff68", "#eb3203"],
        range_color=(0, 500),
        featureidkey="properties.name",
        mapbox_style="carto-positron",
        zoom=5.6,
        center={"lat": -22.5, "lon": -48},
        opacity=0.5,
        labels={"city": "Cidade", "Quantidade de Processos": "Quantidade de Processos"},
        hover_data=["city", "Quantidade de Processos"],
    )

    fig.update_layout(margin={"r": 5, "t": 5, "l": 5, "b": 5})
    return fig


def _select_most_and_amount_attribute(df, attribute):
    att, counts = np.unique(
        sum(
            [
                sub.replace("]", "").replace("[", "").replace("'", "").split(", ")
                for sub in df[attribute]
            ],
            [],
        ),
        return_counts=True,
    )
    count_sort_ind = np.argsort(-counts)
    most_att, most_att_amount = att[count_sort_ind][0], counts[count_sort_ind][0]
    return most_att, most_att_amount


def _count_time(df):
    times = sum([sub.replace("]", "").replace("[", "").replace("'", "").split(", ") for sub in df["Tempo Total em dias"]], [],)
    times = [int(t) for t in times]
    
    total_time = round(np.mean(times), 1)

    return total_time

def update_cards_visao_geral(value_city):
    df_plot = _filter_df(value_city)

    if len(df_plot["Assunto"]) == 0:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    lawsuits_amount = df_plot["Quantidade de Processos"].sum()

    most_subject, most_subject_amount = _select_most_and_amount_attribute(
        df_plot, "Assunto"
    )
    most_classes, most_classes_amount = _select_most_and_amount_attribute(
        df_plot, "Classe"
    )
    most_type, most_type_amount = _select_most_and_amount_attribute(df_plot, "Tipo")
    most_court, most_court_amount = _select_most_and_amount_attribute(df_plot, "Vara")
    most_judge, most_judge_amount = _select_most_and_amount_attribute(df_plot, "Juiz")
    most_clerk, most_clerk_amount = _select_most_and_amount_attribute(
        df_plot, "Escrivão"
    )
    total_time = _count_time(df_plot)

    return (
        lawsuits_amount,
        most_subject,
        most_subject_amount,
        most_classes,
        most_classes_amount,
        most_type,
        most_type_amount,
        most_court,
        most_court_amount,
        most_judge,
        most_judge_amount,
        most_clerk,
        most_clerk_amount,
        total_time
    )
