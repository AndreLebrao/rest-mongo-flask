import os
import requests
import xmltodict
from unidecode import unidecode
from flask import Flask, abort, jsonify


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/health")
    def health():
        return "OK!"

    @app.route("/api/v1/forecast/<string:cep>",methods=["POST"])
    def forecast(cep):
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

    return app
    
