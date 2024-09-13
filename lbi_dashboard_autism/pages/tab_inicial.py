from dash import html

TAB_INICIAL_PAGE = (
    html.Div(
        [
            html.Div(
                [
                    html.Img(
                        src="./assets/img/logo_usp.png",
                        style={
                            "height": "80px",
                            "width": "195px",
                            "padding": "15px",
                        },
                    ),
                    html.Img(
                        src="./assets/img/logo_fearp.png",
                        style={
                            "height": "112px",
                            "width": "150px",
                            "padding": "15px",
                        },
                    ),
                    html.Img(
                        src="./assets/img/logo_habeas_data.png",
                        style={
                            "height": "89px",
                            "width": "400px",
                            "padding": "15px",
                        },
                    ),
                ],
                style={
                    "display": "flex",
                    "flex-direction": "row",
                    "height": "100%",
                    "width": "100%",
                    "justify-content": "space-around",
                },
            ),
            html.H4(
                children="TETSSE PARA VISUALIZAÇÃO DE DADOS PROCESSUAIS DA LEI BRASILEIRA DE INCLUSÃO",
                style={
                    "textAlign": "center",
                    "color": "#252423",
                    "margin-bottom": "10px",
                    "font-weight": "bold",
                    "font-size": "28px",
                },
            ),
            html.P(
                [
                    "Discente: Luiz Henrique Alves do Nascimento",
                    html.Br(),
                    "Orientador: Prof. Dr. Ildeberto A. Rodello",
                ],
                style={
                    "textAlign": "right",
                    "color": "#252423",
                    "font-weight": "normal",
                    "font-size": "22px",
                    "margin-bottom": "10px",
                    "padding": "5px",
                },
            ),
            html.Label(
                children='O presente painel é o resultado do projeto de pesquisa PUB entitulado de "Projeto e Implementação de Um Painel para Análise de Dados de uma Base de Dados de Decisões Judiciais" pela Faculdade de Economia, Administração e Contabilidade de Ribeirão Preto da Universidade de São Paulo que se apoia no projeto desenvolvido pelo graduado em administração Murilo Torres Andrade denominado de "Projeto e Implementação de painéis para Visualização de Dados Processuais". A base de dados processuais utilizada foi disponibilizada pelo grupo de pesquisa Habeas Data, da mesma faculdade. Ela contém os dados processuais ligados à Lei Brasileira de Inclusão (LBI), Lei n. 13.146/2015, mais precisamente o Título 4 que discorre a cerca da "Tutela", da "Curatela" e da "Tomada de Decisão Apoiada”, instrumentos que visam garantir à pessoa com deficiência maior autonomia. Os processos são referentes às palavras-chave: "Tutela","Curatela" e "Decisão Apoiada" com um recorte temporal dos 5 anos após a vigência da lei (2016-2021) e aos 5 anos anteriores (2011-2016).',
                style={
                    "textAlign": "justify",
                    "color": "#252423",
                    "font-weight": "normal",
                    "font-size": "22px",
                    "padding": "5px",
                },
            ),
        ],
        style={
            "display": "grid",
            "grid-template-columns": "1fr",
            "grid-template-rows": "1fr 1fr 1fr",
            "gap": "5px",
            "background-color": "#fff",
            "border-radius": "15px",
            "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
            "padding": "10px",
            "margin-top": "10px",
            "margin-bottom": "10px",
        },
    ),
)
