from flask import jsonify, request, Blueprint
from tables import payment_methods
from tables.contributions import (
    Contributions,
    contribution_schema,
    contributions_schema,
    ContributionsSchema,
)
from db import db

contrib = Blueprint("contrib", __name__)


@contrib.route("/contrib/get/all", methods=["GET"])
def get_all_active_np_route():
    np = db.session.query(Contributions).filter(Contributions.active == True).all()

    if np:
        return jsonify(contributions_schema.dump(np)), 200
    else:
        return jsonify("No matching records"), 404


@contrib.route("/contrib/add", methods=["POST"])
def np_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403
    user_id = post_data.get("user_id")
    np_id = post_data.get("np_id")
    payment_method_id = post_data.get("payment_method_id")
    amount_contributed = post_data.get("amount_contributed")
    roundup_on_off = post_data.get("roundup_on_off")

    if (
        user_id
        and np_id
        and payment_method_id
        and amount_contributed
        and roundup_on_off
    ):

        new_contrib = Contributions(
            user_id,
            np_id,
            payment_method_id,
            amount_contributed,
            roundup_on_off,
        )
        db.session.add(new_contrib)
        db.session.commit()

        return jsonify("Non Profit Organization created"), 201
    else:
        return jsonify("Missing critical information for creation"), 403
