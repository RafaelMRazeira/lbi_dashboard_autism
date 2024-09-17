import pandas as pd
from dash import html, dcc
import plotly.express as px
from unidecode import unidecode
from lbi_dashboard_autism.const import ESTADOS, LOCALIZACAO, BRAZIL_GEOJSON
from lbi_dashboard_autism.data import DF_DADOS_MAPA, DF_LBI_FILTER, DADOS_CENSO

TAB_DEMANDAS_PAGE = html.Div(
    [
        html.Div(
            [
                # FILTROS
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label(
                                    "FILTRAR POR ESTADO",
                                    style={
                                        "marginBottom": "5px",
                                        "fontSize": "12px",
                                    },
                                ),
                                dcc.Dropdown(
                                    ESTADOS,
                                    multi=True,
                                    clearable=True,
                                    id="filter-state",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "width": "100%",
                                "marginRight": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "FILTRAR POR REGIÃO",
                                    style={
                                        "marginBottom": "5px",
                                        "fontSize": "12px",
                                    },
                                ),
                                dcc.Dropdown(
                                    list(LOCALIZACAO.keys()),
                                    multi=True,
                                    clearable=True,
                                    id="filter-region",
                                ),
                            ],
                            style={
                                "display": "flex",
                                "flexDirection": "column",
                                "width": "100%",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "row",
                    },
                ),
                # MÉDIA
                html.Div(
                    [
                        html.H4(
                            children="Quantidade de Processos a cada 100 mil habitantes",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "marginBottom": "5px",
                                "fontWeight": "normal",
                                "fontSize": "12px",
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
                            id="process_mil",
                        ),
                    ],
                    style={},
                ),
                # MAPA
                html.Div([html.Div(dcc.Graph(id="choropleth-map-demand"))], style={}),
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
                    dcc.Graph(id="histogram-demand"),
                    style={
                        "backgroundColor": "#fff",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    dcc.Graph(id="bar-demand"),
                    style={
                        "backgroundColor": "#fff",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                        "padding": "10px",
                    },
                ),
            ],
            style={
                "display": "grid",
                "grid-template-columns": "1fr",
                "grid-template-rows": "1fr 1fr",
                "gap": "10px",
            },
        ),
    ],
    style={
        "display": "grid",
        "grid-template-columns": "1fr 1fr",
        "gap": "10px",
        "padding": "10px",
        "fontFamily": "Open Sans, sans-serif",
    },
)


def update_map_demanda(value_state, value_region):

    df_map = pd.DataFrame()

    df_dados_mapa_merge = DF_DADOS_MAPA.copy()
    df_dados_mapa_merge["Estado"] = DF_DADOS_MAPA["Estado"].apply(unidecode)

    df_censo_merge = DADOS_CENSO[["ESTADO", "UF", "POPULAÇÃO / 100K"]].copy()
    df_censo_merge.rename(columns={"ESTADO": "Estado"}, inplace=True)

    df_lbi_merge = DF_LBI_FILTER["ESTADOS"].value_counts().to_frame()
    df_lbi_merge.index.names = ["Estado"]

    df_censo_merge = pd.merge(df_censo_merge, df_lbi_merge, how="inner", on="Estado")
    df_censo_merge.rename(columns={"count": "Processos"}, inplace=True)

    df_dados_mapa_final = pd.merge(
        df_dados_mapa_merge, df_censo_merge, how="inner", on="Estado"
    )

    df_dados_mapa_final["PROCESSOS / 100K"] = (
        df_dados_mapa_final["Processos"] / df_dados_mapa_final["POPULAÇÃO / 100K"]
    )

    fig = px.choropleth_mapbox(
        df_dados_mapa_final,
        locations="Estado",
        geojson=BRAZIL_GEOJSON,
        color="PROCESSOS / 100K",
        hover_name="Estado",
        hover_data=["PROCESSOS / 100K", "Longitude", "Latitude"],
        title="Quantidade de Processos a cada 100 mil habitantes por Estado",
        mapbox_style="white-bg",
        labels={"PROCESSOS / 100K": "Processos por 100 mil"},
        center={"lat": -14, "lon": -55},
        zoom=2,
        color_continuous_scale="Teal",
    )

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:

                df_map = pd.concat(
                    [
                        df_map,
                        df_dados_mapa_final.loc[
                            (df_dados_mapa_final["Região"] == regiao)
                        ],
                    ]
                )

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_map = pd.concat(
                    [
                        df_map,
                        df_dados_mapa_final.loc[
                            (df_dados_mapa_final["Estado"] == unidecode(estado))
                        ],
                    ]
                )
        else:
            for estado in value_state:
                for regiao in value_region:
                    df_map = pd.concat(
                        [
                            df_map,
                            df_dados_mapa_final.loc[
                                (
                                    (df_dados_mapa_final["Estado"] == unidecode(estado))
                                    & (df_dados_mapa_final["Região"] == regiao)
                                )
                            ],
                        ]
                    )

        if df_map.empty:
            fig = px.choropleth_mapbox(
                df_map,
                geojson=BRAZIL_GEOJSON,
                title="Quantidade de Processos a cada 100 mil habitantes por Estado",
                mapbox_style="white-bg",
                center={"lat": -14, "lon": -55},
                zoom=2,
                color_continuous_scale="Teal",
                labels={"PROCESSOS / 100K": "Processos por 100 mil"},
            )

            return fig

        fig = px.choropleth_mapbox(
            df_map,
            locations="Estado",
            geojson=BRAZIL_GEOJSON,
            color="PROCESSOS / 100K",
            hover_name="Estado",
            hover_data=["PROCESSOS / 100K", "Longitude", "Latitude"],
            title="Quantidade de Processos a cada 100 mil habitantes por Estado",
            mapbox_style="white-bg",
            labels={"PROCESSOS / 100K": "Processos por 100 mil"},
            center={"lat": -14, "lon": -55},
            zoom=2,
            color_continuous_scale="Teal",
        )

        return fig
    else:
        return fig


def update_cards_demand(value_state, value_region):

    total_habitantes = 0
    total_cases = 0

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:
                df_lbi_2 = DF_LBI_FILTER.loc[(DF_LBI_FILTER["regiao"] == regiao)]
                dados_censo_2 = DADOS_CENSO.loc[(DADOS_CENSO["REGIAO"] == regiao)]

                total_cases += df_lbi_2["_id"].nunique()
                total_habitantes += dados_censo_2["POPULAÇÃO / 100K"].sum()

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_lbi_2 = DF_LBI_FILTER.loc[
                    (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                ]
                dados_censo_2 = DADOS_CENSO.loc[
                    (DADOS_CENSO["ESTADO"] == unidecode(estado))
                ]

                total_cases += df_lbi_2["_id"].nunique()
                total_habitantes += dados_censo_2["POPULAÇÃO / 100K"].sum()
        else:
            for regiao in value_region:
                for estado in value_state:
                    df_lbi_2 = DF_LBI_FILTER.loc[
                        (
                            (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                            & (DF_LBI_FILTER["regiao"] == regiao)
                        )
                    ]
                    dados_censo_2 = DADOS_CENSO.loc[
                        (
                            (DADOS_CENSO["ESTADO"] == unidecode(estado))
                            & (DADOS_CENSO["REGIAO"] == regiao)
                        )
                    ]

                    total_cases += df_lbi_2["_id"].nunique()
                    total_habitantes += dados_censo_2["POPULAÇÃO / 100K"].sum()

        if total_cases == 0:
            return "0"
        else:

            return f"{(total_cases/total_habitantes):.2f}".format().replace(".", ",")
    else:
        return f"{DF_LBI_FILTER['_id'].nunique()/DADOS_CENSO['POPULAÇÃO / 100K'].sum():.2f}".format().replace(
            ".", ","
        )


def update_bar_stacked_demand(value_state, value_region):

    df_bar_filter = pd.DataFrame()

    df_bar = DF_LBI_FILTER.copy()

    df_bar = df_bar.groupby(["ano de inicio", "status"]).size().unstack(fill_value=0)
    df_bar.reset_index(inplace=True)
    df_bar["ano de inicio"] = pd.to_datetime(df_bar["ano de inicio"], format="%Y")

    fig = px.bar(
        df_bar,
        x="ano de inicio",
        y=["Sentenciado", "Não Sentenciado"],
        labels={
            "value": "Número de Processos",
            "variable": "Status",
            "ano de inicio": "Ano de Início",
        },
        barmode="stack",
    )

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:

                df_bar_filter = pd.concat(
                    [
                        df_bar_filter,
                        DF_LBI_FILTER.loc[(DF_LBI_FILTER["regiao"] == regiao)],
                    ]
                )

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_bar_filter = pd.concat(
                    [
                        df_bar_filter,
                        DF_LBI_FILTER.loc[
                            (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                        ],
                    ]
                )

        else:
            for estado in value_state:
                for regiao in value_region:
                    df_bar_filter = pd.concat(
                        [
                            df_bar_filter,
                            DF_LBI_FILTER.loc[
                                (
                                    (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                                    & (DF_LBI_FILTER["regiao"] == regiao)
                                )
                            ],
                        ]
                    )

        df_bar_filter = (
            df_bar_filter.groupby(["ano de inicio", "status"])
            .size()
            .unstack(fill_value=0)
        )
        df_bar_filter.reset_index(inplace=True)
        df_bar_filter["ano de inicio"] = pd.to_datetime(
            df_bar_filter["ano de inicio"], format="%Y"
        )

        if df_bar_filter.empty:
            fig = px.bar(
                df_bar_filter,
                x="ano de inicio",
                y=["Sentenciado", "Não Sentenciado"],
                labels={
                    "value": "Número de Processos",
                    "variable": "Status",
                    "ano de inicio": "Ano de Início",
                },
                barmode="stack",
            )

            return fig

        fig = px.bar(
            df_bar_filter,
            x="ano de inicio",
            y=["Sentenciado", "Não Sentenciado"],
            labels={
                "value": "Número de Processos",
                "variable": "Status",
                "ano de inicio": "Ano de Início",
            },
            barmode="stack",
        )

        return fig
    else:
        return fig


def update_bar_demand(value_state, value_region):

    df_bar_filter = pd.DataFrame()

    df_bar = DF_LBI_FILTER.copy()

    df_bar = df_bar["comarca"].value_counts().to_frame()
    df_bar.index.names = ["Comarca"]
    df_bar = df_bar.reset_index()
    df_bar = df_bar.sort_values(by="count").tail(10)

    fig = px.bar(
        df_bar,
        x="count",
        y="Comarca",
        orientation="h",
        title="Comarcas com Maior Número de Processos",
        labels={"count": "", "Comarca": ""},
    )

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:

                df_bar_filter = pd.concat(
                    [
                        df_bar_filter,
                        DF_LBI_FILTER.loc[(DF_LBI_FILTER["regiao"] == regiao)],
                    ]
                )

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_bar_filter = pd.concat(
                    [
                        df_bar_filter,
                        DF_LBI_FILTER.loc[
                            (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                        ],
                    ]
                )

        else:
            for estado in value_state:
                for regiao in value_region:
                    df_bar_filter = pd.concat(
                        [
                            df_bar_filter,
                            DF_LBI_FILTER.loc[
                                (
                                    (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                                    & (DF_LBI_FILTER["regiao"] == regiao)
                                )
                            ],
                        ]
                    )

        df_bar_filter = df_bar_filter["comarca"].value_counts().to_frame()
        df_bar_filter.index.names = ["Comarca"]
        df_bar_filter = df_bar_filter.reset_index()
        df_bar_filter = df_bar_filter.sort_values(by="count").tail(10)

        if df_bar_filter.empty:
            fig = px.bar(
                df_bar_filter,
                x="count",
                y="Comarca",
                orientation="h",
                title="Comarcas com Maior Número de Processos",
                labels={"count": "", "Comarca": ""},
            )

            return fig

        fig = px.bar(
            df_bar_filter,
            x="count",
            y="Comarca",
            orientation="h",
            title="Comarcas com Maior Número de Processos",
            labels={"count": "", "Comarca": ""},
        )

        return fig
    else:
        return fig
