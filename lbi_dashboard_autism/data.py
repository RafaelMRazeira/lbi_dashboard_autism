import numpy as np
import pandas as pd
from lbi_dashboard_autism.const import UF_TO_REGION

# Importação dos dados
DF_LBI = pd.read_csv("./assets/data/admin_HD_LBI.csv")
DF_DADOS_MAPA = pd.read_csv("./assets/data/dados_mapa.csv")
DADOS_CENSO = pd.read_csv("./assets/data/dados_censo.csv")

# Correções
DF_LBI["regiao"] = DF_LBI.apply(
    lambda row: UF_TO_REGION.get(row["UF"], row["regiao"]), axis=1
)
DF_LBI["Tempo de Processo em Anos"] = (
    DF_LBI["Tempo de Processo em Anos"]
    .str.replace(",", ".")
    .astype(float)
    .apply(lambda x: np.nan if x < 0 else x)
)

DADOS_CENSO = DADOS_CENSO.drop(
    columns=["PROCESSOS POR 100MIL HABITANTES", "Quantidade de Processos por Estado"]
)
DADOS_CENSO["POPULAÇÃO / 100K"] = (
    DADOS_CENSO["POPULAÇÃO / 100K"].str.replace(",", ".").astype(float)
)
DADOS_CENSO["REGIAO"] = DADOS_CENSO["REGIAO"].str.replace("Região ", "")

# Filtros - Escopo Temporal
DF_LBI_FILTER = DF_LBI[
    DF_LBI["numero"].str.split(".").str[1].isin([str(ano) for ano in range(2011, 2022)])
]
