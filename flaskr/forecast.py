from flask import abort, jsonify
import requests
from unidecode import unidecode
import xmltodict

def city_forecast_from_cep(cep):
    viacep_url = f"https://viacep.com.br/ws/{cep}/json"
    viacep_response = requests.request("GET",viacep_url)
    viacep_data = viacep_response.json()

    raw_city_name = viacep_data.get("localidade","")
    if(raw_city_name ==""):
        abort(422)
    # removes any special characters and only lower case letters, INPE standards according to their docs
    city_name = unidecode(raw_city_name).lower()

    inpe_base_url = "http://servicos.cptec.inpe.br/XML/"

    city_search_url = f"{inpe_base_url}listaCidades?city={city_name}"
    city_search_response = requests.request("GET", city_search_url)
    all_cities_data = xmltodict.parse(xml_input=city_search_response.content,encoding="ISO-8859-1")
    city_id = all_cities_data["cidades"]["cidade"][0]["id"]
    

    city_forecast_url = f"{inpe_base_url}/cidade/{city_id}/previsao.xml"
    city_forecast_response = requests.request("GET", city_forecast_url)
    city_forecast_data = xmltodict.parse(xml_input=city_forecast_response.content,encoding="ISO-8859-1")

    forecast_response = jsonify(
        viacep = viacep_data,
        inpe = city_forecast_data
    )

    return forecast_response