from flask import jsonify, request, Blueprint
from tables import payment_methods
from tables.contributions import Contributions
from tables.schemas import contribution_schema, contributions_schema

from db import db

contrib = Blueprint("contrib", __name__)


@contrib.route("/contrib/get/all", methods=["GET"])
def get_all_contribs_route():
    np = db.session.query(Contributions).all()

    if np:
        return jsonify(contributions_schema.dump(np)), 200
    else:
        return jsonify("No matching records"), 404


@contrib.route("/contrib/add", methods=["POST"])
def contrib_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403

    required_fields = [
        "user_id",
        "np_id",
        "payment_method_id",
        "amount_contributed",
        "roundup_on_off",
    ]

    post_data = dict(post_data)
    missing_fields = []
    for field in required_fields:
        if field not in post_data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify(f"{missing_fields} not found"), 404

    new_contrib = Contributions(
        post_data["user_id"],
        post_data["np_id"],
        post_data["payment_method_id"],
        post_data["amount_contributed"],
        post_data["roundup_on_off"],
    )

    db.session.add(new_contrib)
    db.session.commit()

    return jsonify("Contribution Added"), 201
