import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from models import Base, Sneaker

# App init
app = Flask("Sneakers API")
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB init
db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app, db)


# Errors
@app.errorhandler(404)
def page_not_found(e):
  # note that we set the 404 status explicitly
  response = {'items': [], 'errors': ['Not found']}
  return jsonify(response), 404


@app.errorhandler(500)
def internal_server_error(e):
  # note that we set the 500 status explicitly
  response = {'items': [], 'errors': ['Internal server error']}
  return jsonify(response), 500


# @app.errorhandler(HTTPException)
# def handle_exception(e):
#   """Return JSON instead of HTML for HTTP errors."""
#   # start with the correct headers and status code from the error
#   response = e.get_response()
#   # replace the body with JSON
#   response.data = json.dumps({
#       "code": e.code,
#       "name": e.name,
#       "description": e.description,
#   })
#   response.content_type = "application/json"
#   return response


@app.errorhandler(Exception)
def handle_exception(e):
  # pass through HTTP errors
  if isinstance(e, HTTPException):
    return e

  # now you're handling non-HTTP exceptions only
  response = {'items': [], 'errors': ['Internal server error']}
  return jsonify(response), 500


# Routes
@app.route("/")
def hello():
  return "Welcome to Sneakers API!<br />Endpoints:<br /> - GET /v1/sneakers<br /> - GET /v1/sneakers/$id"


@app.route("/v1/sneakers", methods=["GET"])
def get_all():
  sneakers = db.session.query(Sneaker).order_by(Sneaker.id).limit(10).all()
  response = {
      'items': [s.serialize() for s in sneakers],
      'errors': []
  }
  return jsonify(response)


@app.route("/v1/sneakers/<id_>")
def get_by_id(id_):
  sneaker = db.session.query(Sneaker).filter_by(id=id_).one_or_none()
  response = {'items': [], 'errors': []}
  if sneaker is None:
    response['errors'].append('Sneaker not found')
    return jsonify(response), 404

  response['items'].append(sneaker.serialize())

  return jsonify(response)


# Main
if __name__ == '__main__':
  app.run()
