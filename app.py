import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from models import Sneaker

@app.route("/")
def hello():
  return "Welcome to Sneakers API!<br/>Endpoints:<br/> - GET /v1/sneakers<br/> - POST /v1/sneakers"

@app.route("/v1/sneakers", methods=["POST"])
def add_sneaker():
  name=request.args.get('name')
  brand=request.args.get('brand')
  release_date=request.args.get('release_date')
  try:
    sneaker=Sneaker(
      name=name,
      brand=brand,
      release_date=release_date
    )
    db.session.add(sneaker)
    db.session.commit()
    return "Sneaker added. sneaker id={}".format(sneaker.id)
  except Exception as e:
    return(str(e))

@app.route("/v1/sneakers", methods=["GET"])
def get_all():
  try:
    sneakers=Sneaker.query.all()
    return jsonify([s.serialize() for s in sneakers])
  except Exception as e:
    return(str(e))

# @app.route("/get/<id_>")
# def get_by_id(id_):
#   try:
#     book=Book.query.filter_by(id=id_).first()
#     return jsonify(book.serialize())
#   except Exception as e:
#     return(str(e))

if __name__ == '__main__':
  app.run()