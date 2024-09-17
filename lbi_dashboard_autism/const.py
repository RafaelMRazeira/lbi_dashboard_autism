import os
import pwd
import json
from unidecode import unidecode
from dotenv import dotenv_values
from urllib.request import urlopen

CONFIG = dotenv_values(".env")

LOCALIZACAO = {
    "Norte": ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins"],
    "Nordeste": [
        "Alagoas",
        "Bahia",
        "Ceará",
        "Maranhão",
        "Paraíba",
        "Pernambuco",
        "Piauí",
        "Rio Grande do Norte",
        "Sergipe",
    ],
    "Centro-Oeste": ["Distrito Federal", "Goiás", "Mato Grosso", "Mato Grosso do Sul"],
    "Sudeste": ["Espírito Santo", "Minas Gerais", "Rio de Janeiro", "São Paulo"],
    "Sul": ["Paraná", "Rio Grande do Sul", "Santa Catarina"],
}

ESTADOS = [
    "Acre",
    "Alagoas",
    "Amapa",
    "Amazonas",
    "Bahia",
    "Ceará",
    "Distrito Federal",
    "Espirito Santo",
    "Goias",
    "Maranhão",
    "Mato Grosso",
    "Mato Grosso do Sul",
    "Minas Gerais",
    "Para",
    "Paraíba",
    "Parana",
    "Pernambuco",
    "Piaui",
    "Rio de Janeiro",
    "Rio Grande do Norte",
    "Rio Grande do Sul",
    "Rondonia",
    "Roraima",
    "Santa Catarina",
    "São Paulo",
    "Sergipe",
    "Tocantins",
]

UF_TO_REGION = {
    "AC": "Norte",
    "AL": "Nordeste",
    "AP": "Norte",
    "AM": "Norte",
    "BA": "Nordeste",
    "CE": "Nordeste",
    "DF": "Centro-Oeste",
    "ES": "Sudeste",
    "GO": "Centro-Oeste",
    "MA": "Nordeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "MG": "Sudeste",
    "PA": "Norte",
    "PB": "Nordeste",
    "PR": "Sul",
    "PE": "Nordeste",
    "PI": "Nordeste",
    "RJ": "Sudeste",
    "RN": "Nordeste",
    "RS": "Sul",
    "RO": "Norte",
    "RR": "Norte",
    "SC": "Sul",
    "SP": "Sudeste",
    "SE": "Nordeste",
    "TO": "Norte",
}

with urlopen(
    "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"
) as response:
    Brazil = json.load(response)

state_id_map = {}

for feature in Brazil["features"]:
    feature["id"] = unidecode(feature["properties"]["name"])
    state_id_map[feature["properties"]["sigla"]] = feature["id"]

BRAZIL_GEOJSON = Brazil.copy()

TIMEOUT = 900

USERNAME = pwd.getpwuid(os.getuid())[0]


def _lower_case_city_geojson(sp_geojson):
    for city_sp_geojson in sp_geojson["features"]:
        city_sp_geojson["properties"]["name"] = city_sp_geojson["properties"][
            "name"
        ].lower()
    return sp_geojson


def load_cities_sp_geojson():
    f = open("assets/data/all_cities_sao_paulo_geo_location.json", "r")
    cities_sp_geojson = json.load(f)
    cities_sp_geojson = _lower_case_city_geojson(cities_sp_geojson)
    all_cities = [
        city["properties"]["name"].lower() for city in cities_sp_geojson["features"]
    ]
    return cities_sp_geojson, all_cities


CITIES_SP_GEOJSON, ALL_CITIES_SP = load_cities_sp_geojson()

EXTERNAL_STYLESHEETS = [
    "https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap",
]
