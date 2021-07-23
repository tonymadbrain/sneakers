import os
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException
from models import Base, Sneaker, Image, Link, Source

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


@app.errorhandler(405)
def method_not_allowed(e):
  response = {'items': [], 'errors': ['Method not allowed']}
  return jsonify(response), 405


@app.errorhandler(500)
def internal_server_error(e):
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


# @app.errorhandler(Exception)
# def handle_exception(e):
#   # pass through HTTP errors
#   if isinstance(e, HTTPException):
#     return e

#   print(f"Unexpected error: { str(e) }")
#   # now you're handling non-HTTP exceptions only
#   response = {'items': [], 'errors': ['Internal server error']}
#   return jsonify(response), 500


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


@app.route("/v1/sneakers", methods=["POST"])
def post():
  response = {
      'items': [],
      'errors': []
  }

  source = db.session.query(Source).filter_by(name='Sneaker API').one_or_none()
  if not source:
    source = Source(
        name='Sneakers API'
    )
    try:
      db.session.add(source)
      db.session.commit()
    except Exception as e:
      db.session.rollback()
      raise e

  body = request.get_json()
  image_body = body.pop('image')
  links_body = body.pop('links')
  try:
    image = Image(**image_body)
    links = Link(**links_body)
    db.session.commit()
    sneaker = Sneaker(**body, image=image, links=links, source=source)
    db.session.commit()
    sneaker.id_in_source = sneaker.id
    db.session.commit()
    response['items'].append({'id': sneaker.id})
    return jsonify(response), 201
  except TypeError as e:
    db.session.rollback()
    response['errors'].append('Wrong fields')
    response['errors'].append(str(e))
    return jsonify(response), 400
  # except (FieldDoesNotExist, ValidationError):
  #   raise SchemaValidationError
  # except NotUniqueError:
  #   raise MovieAlreadyExistsError
  except Exception as e:
    # raise InternalServerError
    db.session.rollback()
    raise e


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
