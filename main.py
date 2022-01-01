from config import create_app
from db import db

app = create_app()


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


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
