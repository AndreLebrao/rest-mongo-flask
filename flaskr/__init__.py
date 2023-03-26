from flask import Flask
from . import forecast

def create_app():
    # create and configure the app
    app = Flask(__name__)

    @app.route("/health")
    def health():
        return "OK!"

    @app.route("/api/v1/forecast/<string:cep>",methods=["POST"])
    def city_forecast(cep):
        return forecast.city_forecast_from_cep(cep)

    return app
    
