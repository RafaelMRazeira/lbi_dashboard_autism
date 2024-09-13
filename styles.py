from dash import html, dcc

EXTERNAL_STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
]

LAYOUT = html.Div(
    [
        html.Div(
            dcc.Tabs(
                id="tabs-LBI",
                value="tab-inicial",
                children=[
                    dcc.Tab(label="Início", value="tab-inicial"),
                    dcc.Tab(label="Visão Geral", value="tab-visao_geral"),
                    dcc.Tab(label="Duração", value="tab-duracao"),
                    dcc.Tab(label="Demandas", value="tab-demandas"),
                ],
            ),
            style={"font-weight": "bold", "font-family": "Raleway, sans-serif"},
        ),
        html.Div(id="tabs-content"),
    ],
    style={"margin-top": "10px"},
)
