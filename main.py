from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from werkzeug.exceptions import BadRequest

from config import DevelopmentConfig
from db import db
from resources.routes import routes

# this WSGI app is an instance of class Flask
app = Flask(__name__)

# configuring flask app and db connection string
app.config.from_object(DevelopmentConfig)

# initialize db
db.init_app(app)

# allow changing column type
migrate = Migrate(compare_type=True)
migrate.init_app(app, db)

# api wraps app, makes it a Restful API
api = Api(app)

# Adding resources for endpoints in routes.py
[api.add_resource(*r) for r in routes]

#
# @app.after_request
# def conclude_request(response):
#     # before sending response to Postman
#     try:
#         db.session.commit()
#     except Exception as ex:
#         raise BadRequest(f'{ex}')
#     return response


# this is entering point of our project
if __name__ == "__main__":
    app.run()
    #   app.run(debug=DEBUG, host=HOST, port=PORT)
