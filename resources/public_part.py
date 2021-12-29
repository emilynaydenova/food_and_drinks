from flask import request
from flask_restful import Resource

from managers.food_and_drinks import FoodAndDrinksManager
from schemas.response.food_and_drinks import FoodAndDrinksResponseSchema
from services.rapid_api.weather import CurrentWeatherService

weather = CurrentWeatherService()


class PublicView(Resource):
    """
    Get all food_and_drinks by category and return only available ones.
    the path must include query ->  ?category='some enum value'
    The weather conditions at the local place are included in the response.
    """

    @staticmethod
    def get():
        args = request.args
        foods = FoodAndDrinksManager.get_all_food_and_drinks_by_category(args)
        current_weather = weather.get_weather()  # dict
        merged_dict = {
            key: value for (key, value) in (foods.items() + current_weather.items())
        }
        # json.dumps(merged_dict)
        schema = FoodAndDrinksResponseSchema()
        return schema.dump(foods, many=True)
