import pandas as pd
from dash import html, dcc
import plotly.express as px
from unidecode import unidecode
from lbi_dashboard_autism.data import DF_DADOS_MAPA, DF_LBI_FILTER
from lbi_dashboard_autism.const import ESTADOS, LOCALIZACAO, BRAZIL_GEOJSON


TAB_DURACAO_PAGE = html.Div(
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
                            children="Média de Tempo dos Processos",
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
                            id="avg_process",
                        ),
                        html.P(
                            " anos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "marginTop": "5px",
                                "margin-left": "62px",
                                "fontWeight": "bold",
                            },
                        ),
                    ],
                    style={},
                ),
                # MAPA
                html.Div(
                    [html.Div(dcc.Graph(id="choropleth-map-duration"))],
                    style={},
                ),
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
                    dcc.Graph(id="scatter-duration"),
                    style={
                        "backgroundColor": "#fff",
                        "borderRadius": "15px",
                        "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                        "padding": "10px",
                    },
                ),
                html.Div(
                    [
                        html.Div(dcc.Graph(id="bar-duration")),
                        html.Div(
                            [
                                html.H4(
                                    children="Processos Sentenciados",
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
                                    id="avg_process_sentenced",
                                ),
                                html.P(
                                    "dos processos",
                                    style={
                                        "textAlign": "center",
                                        "color": "#252423",
                                        "fontSize": 12,
                                        "marginTop": "5px",
                                        "margin-left": "62px",
                                        "fontWeight": "bold",
                                    },
                                ),
                            ],
                            style={},
                        ),
                    ],
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


def update_map_duracao(value_state, value_region):

    df_map = pd.DataFrame()

    df_dados_mapa_merge = DF_DADOS_MAPA.copy()
    df_dados_mapa_merge["Estado"] = DF_DADOS_MAPA["Estado"].apply(unidecode)

    df_lbi_merge = DF_LBI_FILTER[["ESTADOS", "Tempo de Processo em Anos"]]
    # df_lbi_merge['Tempo de Processo em Anos'] = df_lbi_merge['Tempo de Processo em Anos'].str.replace(',', '.').astype(float)

    df_lbi_merge = df_lbi_merge.groupby(["ESTADOS"]).mean(numeric_only=True)

    df_lbi_merge.index.names = ["Estado"]

    df_dados_mapa_final = pd.merge(
        df_dados_mapa_merge, df_lbi_merge, how="inner", on="Estado"
    )

    fig = px.choropleth_mapbox(
        df_dados_mapa_final,
        locations="Estado",
        geojson=BRAZIL_GEOJSON,
        color="Tempo de Processo em Anos",
        hover_name="Estado",
        hover_data=["Tempo de Processo em Anos", "Longitude", "Latitude"],
        title="Média de Tempo dos Processos por Estado",
        mapbox_style="white-bg",
        labels={"Tempo de Processo em Anos": "Anos"},
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
                title="Média de Tempo dos Processos por Estado",
                mapbox_style="white-bg",
                center={"lat": -14, "lon": -55},
                zoom=2,
                color_continuous_scale="Teal",
                labels={"Tempo de Processo em Anos": "Anos"},
            )

            return fig

        fig = px.choropleth_mapbox(
            df_map,
            locations="Estado",
            geojson=BRAZIL_GEOJSON,
            color="Tempo de Processo em Anos",
            hover_name="Estado",
            hover_data=["Tempo de Processo em Anos", "Longitude", "Latitude"],
            title="Média de Tempo dos Processos por Estado",
            mapbox_style="white-bg",
            labels={"Tempo de Processo em Anos": "Anos"},
            center={"lat": -14, "lon": -55},
            zoom=2,
            color_continuous_scale="Teal",
        )

        return fig
    else:
        return fig


def update_cards_duration(value_state, value_region):

    avg_process = 0
    total_cases = 0
    total_sentenced = 0

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:
                df_lbi_2 = DF_LBI_FILTER.loc[(DF_LBI_FILTER["regiao"] == regiao)]

                avg_process += df_lbi_2["Tempo de Processo em Anos"].mean(
                    numeric_only=True
                )
                total_cases += df_lbi_2["_id"].nunique()
                total_sentenced += df_lbi_2.loc[
                    df_lbi_2["status"] == "Sentenciado"
                ].shape[0]

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_lbi_2 = DF_LBI_FILTER.loc[
                    (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                ]

                avg_process += df_lbi_2["Tempo de Processo em Anos"].mean(
                    numeric_only=True
                )
                total_cases += df_lbi_2["_id"].nunique()
                total_sentenced += df_lbi_2.loc[
                    df_lbi_2["status"] == "Sentenciado"
                ].shape[0]
        else:
            for regiao in value_region:
                for estado in value_state:
                    df_lbi_2 = DF_LBI_FILTER.loc[
                        (
                            (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                            & (DF_LBI_FILTER["regiao"] == regiao)
                        )
                    ]

                    avg_process += df_lbi_2["Tempo de Processo em Anos"].mean(
                        numeric_only=True
                    )
                    total_cases += df_lbi_2["_id"].nunique()

                    if not df_lbi_2.empty:
                        total_sentenced += df_lbi_2.loc[
                            df_lbi_2["status"] == "Sentenciado"
                        ].shape[0]

        if total_cases == 0:
            return "0", " 0 %"
        else:

            return (
                f"{(avg_process):.2f}".format().replace(".", ","),
                f"{(total_sentenced/total_cases)*100:.2f}".format().replace(".", ",")
                + " %",
            )
    else:
        return (
            f"{DF_LBI_FILTER['Tempo de Processo em Anos'].mean(numeric_only = True):.2f}".format().replace(
                ".", ","
            ),
            f"{(DF_LBI_FILTER.loc[DF_LBI_FILTER['status'] == 'Sentenciado'].shape[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
        )


def update_scatter_duration(value_state, value_region):

    df_scatter_filter = pd.DataFrame()

    df_scatter = DF_LBI_FILTER.copy()

    df_scatter["ESTADOS"] = df_scatter["ESTADOS"].apply(unidecode)

    df_scatter = df_scatter[["ESTADOS", "Tempo de Processo em Anos"]]

    df_scatter_fig = df_scatter.groupby("ESTADOS").agg(
        {"Tempo de Processo em Anos": "mean", "ESTADOS": "count"}
    )

    df_scatter_fig.index.names = ["Estado"]
    df_scatter_fig.columns = [
        "Média de Tempo de Processo em Anos",
        "Quantidade de Processos",
    ]
    df_scatter_fig = df_scatter_fig.reset_index()

    df_scatter_fig["Região"] = df_scatter_fig["Estado"].map(
        {
            unidecode(estado): regiao
            for regiao, estados in LOCALIZACAO.items()
            for estado in estados
        }
    )

    fig = px.scatter(
        df_scatter_fig,
        x="Média de Tempo de Processo em Anos",
        y="Quantidade de Processos",
        hover_name="Estado",
        color="Região",
    )

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:

                df_scatter_filter = pd.concat(
                    [
                        df_scatter_filter,
                        df_scatter_fig.loc[(df_scatter_fig["Região"] == regiao)],
                    ]
                )

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_scatter_filter = pd.concat(
                    [
                        df_scatter_filter,
                        df_scatter_fig.loc[
                            (df_scatter_fig["Estado"] == unidecode(estado))
                        ],
                    ]
                )
        else:
            for estado in value_state:
                for regiao in value_region:
                    df_scatter_filter = pd.concat(
                        [
                            df_scatter_filter,
                            df_scatter_fig.loc[
                                (
                                    (df_scatter_fig["Estado"] == unidecode(estado))
                                    & (df_scatter_fig["Região"] == regiao)
                                )
                            ],
                        ]
                    )

        if df_scatter_filter.empty:
            fig = px.scatter(
                df_scatter_filter,
                x="Média de Tempo de Processo em Anos",
                y="Quantidade de Processos",
                hover_name="Estado",
                color="Região",
            )

            return fig

        fig = px.scatter(
            df_scatter_filter,
            x="Média de Tempo de Processo em Anos",
            y="Quantidade de Processos",
            hover_name="Estado",
            color="Região",
        )

        return fig
    else:
        return fig


def update_bar_duration(value_state, value_region):

    df_bar_filter = pd.DataFrame()

    df_bar = DF_LBI_FILTER.copy()
    df_bar = df_bar.loc[df_bar["sentenca"] != "NÃO CLASSIFICADO"]

    df_bar = df_bar["sentenca"].value_counts().to_frame()
    df_bar.index.names = ["Sentença"]
    df_bar = df_bar.reset_index()

    df_bar = df_bar.sort_values(by="count")

    fig = px.bar(
        df_bar,
        x="count",
        y="Sentença",
        orientation="h",
        labels={"count": "Número de Processos"},
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

        df_bar_filter = df_bar_filter["sentenca"].value_counts().to_frame()
        df_bar_filter.index.names = ["Sentença"]
        df_bar_filter = df_bar_filter.reset_index()

        df_bar_filter = df_bar_filter.sort_values(by="count")

        if df_bar_filter.empty:
            fig = px.bar(
                df_bar_filter,
                x="count",
                y="Sentença",
                orientation="h",
                labels={"count": "Número de Processos"},
            )

            return fig

        fig = px.bar(
            df_bar_filter,
            x="count",
            y="Sentença",
            orientation="h",
            labels={"count": "Número de Processos"},
        )

        return fig
    else:
        return fig
