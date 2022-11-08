from flask import Flask, request, jsonify
from tables import *

from db import *
import routes

app = Flask(__name__)

app.register_blueprint(routes.users)
app.register_blueprint(routes.np)
app.register_blueprint(routes.contrib)
app.register_blueprint(routes.pay)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://johnipson@127.0.0.1:5432/doughnate"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print(app.config)
init_db(app, db)


def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done!")


if __name__ == "__main__":
    create_all()
    app.run(port=8086, host="0.0.0.0")
