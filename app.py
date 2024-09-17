from flask_caching import Cache
from dash import html, dcc, Dash, Output, Input

from lbi_dashboard_autism.utils import get_cache_dir
from lbi_dashboard_autism.const import TIMEOUT, EXTERNAL_STYLESHEETS
from lbi_dashboard_autism.pages.tab_inicial import TAB_INICIAL_PAGE
from lbi_dashboard_autism.pages.tab_visao_geral import (
    TAB_VISAO_GERAL_PAGE,
    update_map_visao_geral,
    update_cards_visao_geral,
)

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
            style={"fontWeight": "bold", "fontFamily": "Raleway, sans-serif"},
        ),
        html.Div(id="tabs-content"),
    ],
    style={"marginTop": "10px"},
)


class DashAPI:

    def __init__(self) -> None:
        self.app = Dash(
            __name__,
            external_stylesheets=EXTERNAL_STYLESHEETS,
            assets_external_path="./assets",
            title="LBI Dashboard",
            update_title="Atualizando ...",
            suppress_callback_exceptions=True,
        )

        self.cache = Cache(
            self.app.server,
            config={"CACHE_TYPE": "filesystem", "CACHE_DIR": get_cache_dir()},
        )

        self.app.layout = LAYOUT
        self.app.css.config.serve_locally = True
        self.app.config.suppress_callback_exceptions = True


dashAPI = DashAPI()


@dashAPI.app.callback(Output("tabs-content", "children"), Input("tabs-LBI", "value"))
# @dashAPI.cache.memoize(timeout=TIMEOUT)
def render_content(tab):

    TABS = {
        "tab-inicial": TAB_VISAO_GERAL_PAGE,
        "tab-visao_geral": TAB_VISAO_GERAL_PAGE,
        "tab-duracao": TAB_INICIAL_PAGE,
        "tab-demandas": TAB_INICIAL_PAGE,
    }

    return TABS.get(tab)


@dashAPI.app.callback(
    Output("choropleth-map-amount", "figure"),
    Input("filter-city", "value"),
)
def _update_map_visao_geral(value_city):
    return update_map_visao_geral(value_city)


@dashAPI.app.callback(
    Output("total_cases", "children"),
    Output("most_subject", "children"),
    Output("amount_most_subject", "children"),
    Output("most_class", "children"),
    Output("amount_most_class", "children"),
    Output("most_type", "children"),
    Output("amount_most_type", "children"),
    Output("most_court", "children"),
    Output("amount_most_court", "children"),
    Output("most_judge", "children"),
    Output("amount_most_judge", "children"),
    Output("most_clerk", "children"),
    Output("amount_most_clerk", "children"),
    Output("total_time", "children"),
    Input("filter-city", "value"),
)
# @dashAPI.cache.memoize(timeout=TIMEOUT)
def _update_cards_visao_geral(value_city):
    return update_cards_visao_geral(value_city)


if __name__ == "__main__":
    dashAPI.app.run(port="8050", debug=True, threaded=True)
