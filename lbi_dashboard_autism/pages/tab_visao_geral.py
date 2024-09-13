import pandas as pd
from dash import html, dcc
import plotly.express as px
from unidecode import unidecode
from lbi_dashboard_autism.data import DF_DADOS_MAPA, DF_LBI_FILTER
from lbi_dashboard_autism.const import ESTADOS, LOCALIZACAO, BRAZIL_GEOJSON

TAB_VISAO_GERAL_PAGE = html.Div(
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
                                        "margin-bottom": "5px",
                                        "font-size": "12px",
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
                                "flex-direction": "column",
                                "width": "100%",
                                "margin-right": "20px",
                            },
                        ),
                        html.Div(
                            [
                                html.Label(
                                    "FILTRAR POR REGIÃO",
                                    style={
                                        "margin-bottom": "5px",
                                        "font-size": "12px",
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
                                "flex-direction": "column",
                                "width": "100%",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                    },
                ),
                # TOTAL
                html.Div(
                    [
                        html.H4(
                            children="Total de Processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "5px",
                                "font-weight": "normal",
                                "font-size": "13px",
                            },
                        ),
                        html.Div(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "font-weight": "bold",
                                "font-size": "32px",
                            },
                            id="total_cases",
                        ),
                    ],
                    style={},
                ),
                # MAPA
                html.Div([html.Div(dcc.Graph(id="choropleth-map-amount"))], style={}),
            ],
            style={
                "background-color": "#fff",
                "border-radius": "15px",
                "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                "padding": "10px",
            },
        ),
        html.Div(
            [
                # Direito civil
                html.Div(
                    [
                        html.H6(
                            children="Área do direito mais presente",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['area_direito'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "15px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_area_direito",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # Família
                html.Div(
                    [
                        html.H6(
                            children="Maior matéria principal",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['materia_principal'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "15px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_materia_principal",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # Processo civil e do trabalho
                html.Div(
                    [
                        html.H6(
                            children="Natureza do processo mais presente",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['natureza_processo'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "13px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_natureza_processo",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # Cível
                html.Div(
                    [
                        html.H6(
                            children="Natureza da vara mais presente",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['natureza_vara'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "15px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_natureza_vara",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # Procedimento de conhecimento
                html.Div(
                    [
                        html.H6(
                            children="Procedimento mais presente",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['procedimento'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "15px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_procedimento",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
                # Processo de conhecimento
                html.Div(
                    [
                        html.H6(
                            children="Tipo de processo mais presente",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "margin-bottom": "3px",
                                "font-weight": "400",
                                "font-size": "14px",
                            },
                        ),
                        html.P(
                            f"{DF_LBI_FILTER['tipo_processo'].value_counts().index.tolist()[0]}",
                            style={
                                "textAlign": "center",
                                "color": "#118DFF",
                                "fontSize": "15px",
                                "font-weight": "bold",
                                "margin-top": "5px",
                                "margin-bottom": "15px",
                            },
                        ),
                        html.P(
                            None,
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": "35px",
                                "margin": "0px",
                            },
                            id="total_tipo_processo",
                        ),
                        html.P(
                            "dos processos",
                            style={
                                "textAlign": "center",
                                "color": "#252423",
                                "fontSize": 12,
                                "margin-top": "5px",
                                "margin-left": "48px",
                                "font-weight": "bold",
                            },
                        ),
                    ],
                    style={
                        "background-color": "#fff",
                        "border-radius": "15px",
                        "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
                    },
                ),
            ],
            style={
                "display": "grid",
                "grid-template-columns": "1fr 1fr",
                "grid-template-rows": "1fr 1fr 1fr",
                "gap": "10px",
            },
        ),
    ],
    style={
        "display": "grid",
        "grid-template-columns": "1fr 1fr",
        "gap": "10px",
        "padding": "10px",
        "font-family": "Open Sans, sans-serif",
    },
)


# ==== Mapas ====
# Visão Geral
def update_map_visao_geral(value_state, value_region):

    df_map = pd.DataFrame()

    df_dados_mapa_merge = DF_DADOS_MAPA.copy()
    df_dados_mapa_merge["Estado"] = DF_DADOS_MAPA["Estado"].apply(unidecode)

    df_lbi_merge = DF_LBI_FILTER["ESTADOS"].value_counts().to_frame()
    df_lbi_merge.index.names = ["Estado"]

    df_dados_mapa_final = pd.merge(
        df_dados_mapa_merge, df_lbi_merge, how="inner", on="Estado"
    )

    fig = px.choropleth_mapbox(
        df_dados_mapa_final,
        locations="Estado",
        geojson=BRAZIL_GEOJSON,
        color="count",
        hover_name="Estado",
        hover_data=["count", "Longitude", "Latitude"],
        title="Quantidade de Processos por Estado",
        mapbox_style="white-bg",
        labels={"count": "Processos"},
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
                title="Quantidade de Processos por Estado",
                mapbox_style="white-bg",
                center={"lat": -14, "lon": -55},
                zoom=2,
                color_continuous_scale="Teal",
                labels={"count": "Processos"},
            )

            return fig

        fig = px.choropleth_mapbox(
            df_map,
            locations="Estado",
            geojson=BRAZIL_GEOJSON,
            color="count",
            hover_name="Estado",
            hover_data=["count", "Longitude", "Latitude"],
            title="Quantidade de Processos por Estado",
            mapbox_style="white-bg",
            labels={"count": "Processos"},
            center={"lat": -14, "lon": -55},
            zoom=2,
            color_continuous_scale="Teal",
        )

        return fig
    else:
        return fig


def update_cards_visao(value_state, value_region):

    total_cases = 0
    total_direito = 0
    total_materia = 0
    total_natureza_processo = 0
    total_natureza_vara = 0
    total_procedimento = 0
    total_tipo = 0

    if (value_state != None and value_state) or (value_region != None and value_region):

        if (value_state == None or not value_state) and (
            value_region != None and value_region
        ):

            for regiao in value_region:
                df_lbi_2 = DF_LBI_FILTER.loc[(DF_LBI_FILTER["regiao"] == regiao)]

                total_cases += df_lbi_2["_id"].nunique()
                total_direito += df_lbi_2["area_direito"].value_counts()[0]
                total_materia += df_lbi_2["materia_principal"].value_counts()[0]
                total_natureza_processo += df_lbi_2["natureza_processo"].value_counts()[
                    0
                ]
                total_natureza_vara += df_lbi_2["natureza_vara"].value_counts()[0]
                total_procedimento += df_lbi_2["procedimento"].value_counts()[0]
                total_tipo += df_lbi_2["tipo_processo"].value_counts()[0]

        elif (value_state != None and value_state) and (
            value_region == None or not value_region
        ):
            for estado in value_state:
                df_lbi_2 = DF_LBI_FILTER.loc[
                    (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                ]

                total_cases += df_lbi_2["_id"].nunique()
                total_direito += df_lbi_2["area_direito"].value_counts()[0]
                total_materia += df_lbi_2["materia_principal"].value_counts()[0]
                total_natureza_processo += df_lbi_2["natureza_processo"].value_counts()[
                    0
                ]
                total_natureza_vara += df_lbi_2["natureza_vara"].value_counts()[0]
                total_procedimento += df_lbi_2["procedimento"].value_counts()[0]
                total_tipo += df_lbi_2["tipo_processo"].value_counts()[0]
        else:
            for regiao in value_region:
                for estado in value_state:
                    df_lbi_2 = DF_LBI_FILTER.loc[
                        (
                            (DF_LBI_FILTER["ESTADOS"] == unidecode(estado))
                            & (DF_LBI_FILTER["regiao"] == regiao)
                        )
                    ]

                    total_cases += df_lbi_2["_id"].nunique()

                    if not df_lbi_2.empty:
                        total_direito += df_lbi_2["area_direito"].value_counts()[0]
                        total_materia += df_lbi_2["materia_principal"].value_counts()[0]
                        total_natureza_processo += df_lbi_2[
                            "natureza_processo"
                        ].value_counts()[0]
                        total_natureza_vara += df_lbi_2["natureza_vara"].value_counts()[
                            0
                        ]
                        total_procedimento += df_lbi_2["procedimento"].value_counts()[0]
                        total_tipo += df_lbi_2["tipo_processo"].value_counts()[0]

        if total_cases == 0:
            return "0", " 0 %", " 0 %", " 0 %", " 0 %", " 0 %", " 0 %"
        else:

            return (
                f"{(total_cases):,}".format().replace(",", "."),
                f"{(total_direito/total_cases)*100:.2f}".format().replace(".", ",")
                + " %",
                f"{(total_materia/total_cases)*100:.2f}".format().replace(".", ",")
                + " %",
                f"{(total_natureza_processo/total_cases)*100:.2f}".format().replace(
                    ".", ","
                )
                + " %",
                f"{(total_natureza_vara/total_cases)*100:.2f}".format().replace(
                    ".", ","
                )
                + " %",
                f"{(total_procedimento/total_cases)*100:.2f}".format().replace(".", ",")
                + " %",
                f"{(total_tipo/total_cases)*100:.2f}".format().replace(".", ",") + " %",
            )
    else:
        return (
            f"{DF_LBI_FILTER['_id'].nunique():,}".format().replace(",", "."),
            f"{(DF_LBI_FILTER['area_direito'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
            f"{(DF_LBI_FILTER['materia_principal'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
            f"{(DF_LBI_FILTER['natureza_processo'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
            f"{(DF_LBI_FILTER['natureza_vara'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
            f"{(DF_LBI_FILTER['procedimento'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
            f"{(DF_LBI_FILTER['tipo_processo'].value_counts()[0])/(DF_LBI_FILTER['_id'].nunique())*100:.2f}".format().replace(
                ".", ","
            )
            + " %",
        )
