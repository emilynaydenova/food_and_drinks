import json

from flask import request
from flask_restful import Resource

from managers.food_and_drinks import FoodAndDrinksManager
from schemas.response.food_and_drinks import FoodAndDrinksResponseSchema
from services.rapid_api.weather import CurrentWeatherService

weather = CurrentWeatherService()


class PublicView(Resource):

    @staticmethod
    def get():
        """
            Get all food_and_drinks by category and return only available ones.
            the path must include query ->  ?category='some enum value'
            The weather conditions at the local place are included in the response.
            """
        args = request.args
        foods = FoodAndDrinksManager.get_all_food_and_drinks_by_category(args)  # list of objects

        schema = FoodAndDrinksResponseSchema()
        resp = schema.dump(foods, many=True)

        current_weather = json.loads(weather.get_weather())  # dict
        resp.append(current_weather)

        return resp
