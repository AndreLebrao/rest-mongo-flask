from flask import Flask
from . import forecast
from flask_restx import Api, Resource
def create_app():
    # create and configure the app
    app = Flask(__name__)
    api = Api(app,doc="/docs", version="1.0", title="rest-mongo-flask",description="A simple application to get forecast data for the next 4 days from a city, given a CEP")
    
    @api.route("/health")
    class Health(Resource):
        def get(self):
            return "OK!"

    @api.route("/api/v1/forecast/<string:cep>")
    class CityForecast(Resource):
        def post(self,cep):
            return forecast.city_forecast_from_cep(cep)

    return app
    
