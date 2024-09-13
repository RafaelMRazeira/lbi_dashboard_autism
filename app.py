from flask_caching import Cache
from dash import Dash, Output, Input

from utils import get_cache_dir
from styles import EXTERNAL_STYLESHEETS, LAYOUT
from lbi_dashboard_autism.const import TIMEOUT
from lbi_dashboard_autism.pages.tab_inicial import TAB_INICIAL_PAGE
from lbi_dashboard_autism.pages.tab_duracao import (
    TAB_DURACAO_PAGE,
    update_map_duracao,
    update_cards_duration,
    update_scatter_duration,
    update_bar_duration,
)
from lbi_dashboard_autism.pages.tab_demandas import (
    TAB_DEMANDAS_PAGE,
    update_map_demanda,
    update_cards_demand,
    update_bar_stacked_demand,
    update_bar_demand,
)
from lbi_dashboard_autism.pages.tab_visao_geral import (
    TAB_VISAO_GERAL_PAGE,
    update_map_visao_geral,
    update_cards_visao,
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


# CallBacks
# ==== Abas ====
@dashAPI.app.callback(Output("tabs-content", "children"), Input("tabs-LBI", "value"))
@dashAPI.cache.memoize(timeout=TIMEOUT)
def render_content(tab):

    TABS = {
        "tab-inicial": TAB_INICIAL_PAGE,
        "tab-visao_geral": TAB_VISAO_GERAL_PAGE,
        "tab-duracao": TAB_DURACAO_PAGE,
        "tab-demandas": TAB_DEMANDAS_PAGE,
    }

    return TABS.get(tab)


@dashAPI.app.callback(
    Output("choropleth-map-amount", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_map_visao_geral(value_state, value_region):
    return update_map_visao_geral(value_state, value_region)


@dashAPI.app.callback(
    Output("choropleth-map-duration", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_map_duracao(value_state, value_region):
    return update_map_duracao(value_state, value_region)


@dashAPI.app.callback(
    Output("choropleth-map-demand", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_map_demanda(value_state, value_region):
    return update_map_demanda(value_state, value_region)


# ==== Cards ====


# Visão Geral
@dashAPI.app.callback(
    Output("total_cases", "children"),
    Output("total_area_direito", "children"),
    Output("total_materia_principal", "children"),
    Output("total_natureza_processo", "children"),
    Output("total_natureza_vara", "children"),
    Output("total_procedimento", "children"),
    Output("total_tipo_processo", "children"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
@dashAPI.cache.memoize(timeout=TIMEOUT)
def _update_cards_visao(value_state, value_region):
    return update_cards_visao(value_state, value_region)


# Duração
@dashAPI.app.callback(
    Output("avg_process", "children"),
    Output("avg_process_sentenced", "children"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
@dashAPI.cache.memoize(timeout=TIMEOUT)
def _update_cards_duration(value_state, value_region):
    return update_cards_duration(value_state, value_region)


# Demandas
@dashAPI.app.callback(
    Output("process_mil", "children"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
@dashAPI.cache.memoize(timeout=TIMEOUT)
def _update_cards_demand(value_state, value_region):
    return update_cards_demand(value_state, value_region)


# ==== Gráficos =====
@dashAPI.app.callback(
    Output("scatter-duration", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_scatter_duration(value_state, value_region):
    return update_scatter_duration(value_state, value_region)


@dashAPI.app.callback(
    Output("bar-duration", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_bar_duration(value_state, value_region):
    return update_bar_duration(value_state, value_region)


@dashAPI.app.callback(
    Output("histogram-demand", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_bar_stacked_demand(value_state, value_region):
    return update_bar_stacked_demand(value_state, value_region)


@dashAPI.app.callback(
    Output("bar-demand", "figure"),
    [Input("filter-state", "value"), Input("filter-region", "value")],
)
def _update_bar_demand(value_state, value_region):
    return update_bar_demand(value_state, value_region)


if __name__ == "__main__":
    dashAPI.app.run(port="8050", debug=True, threaded=True)
