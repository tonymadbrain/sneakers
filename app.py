import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Base, Sneaker

app = Flask("Sneakers API")

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# https://github.com/pallets/flask-sqlalchemy/issues/98
# db.register_base(Base)

migrate = Migrate(app, db)


@app.before_first_request
def setup():
  # Recreate database each time for demo
  # Base.metadata.drop_all(bind=db.engine)
  Base.metadata.create_all(bind=db.engine)
  db.session.commit()


@app.route("/")
def hello():
  return "Welcome to Sneakers API!<br />Endpoints:<br /> - GET /v1/sneakers<br /> - GET /v1/sneakers/$id"


@app.route("/v1/sneakers", methods=["GET"])
def get_all():
  try:
    sneakers = db.session.query(Sneaker).order_by(Sneaker.id).limit(10).all()
    return jsonify([s.serialize() for s in sneakers])
  except Exception as e:
    return(str(e))


@app.route("/v1/sneakers/<id_>")
def get_by_id(id_):
  try:
    sneaker = db.session.query(Sneaker).filter_by(id=id_).first()
    return jsonify(sneaker.serialize())
  except Exception as e:
    return(str(e))


if __name__ == '__main__':
  app.run()
