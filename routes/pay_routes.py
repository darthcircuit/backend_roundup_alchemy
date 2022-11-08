from flask import jsonify, request, Blueprint
from tables.payment_methods import (
    PaymentMethods,
)
from tables.schemas import (
    payment_methods_schema,
    payment_method_types_schema,
    payment_method_schema,
)

from tables.payment_method_types import (
    PaymentMethodTypes,
)
from db import db

pay = Blueprint("pay", __name__)


@pay.route("/payment_method/get/all", methods=["GET"])
def get_all_active_payment_methods():
    np = db.session.query(PaymentMethods).filter(PaymentMethods.active == True).all()

    if np:
        return jsonify(payment_methods_schema.dump(np)), 200
    else:
        return jsonify("No matching records"), 404


@pay.route("/payment_method/add", methods=["POST"])
def pm_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403

    required_fields = [
        "account_name",
        "payment_method_type",
        "account_number",
        "account_owner_phone",
        "billing_street_address",
        "billing_city",
        "billing_state",
        "billing_postal_code",
        "bank_name",
        "bank_routing_num",
        "user_id",
    ]
    post_data = dict(post_data)
    missing_fields = []
    for field in required_fields:
        if field not in post_data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify(f"{missing_fields} not found"), 404

    new_method = PaymentMethods(
        post_data["account_name"],
        post_data["payment_method_type"],
        post_data["account_number"],
        post_data["account_owner_phone"],
        post_data["billing_street_address"],
        post_data["billing_city"],
        post_data["billing_state"],
        post_data["billing_postal_code"],
        post_data["bank_name"],
        post_data["bank_routing_num"],
        post_data["user_id"],
    )
    db.session.add(new_method)
    db.session.commit()

    return jsonify(payment_method_schema.dump(new_method)), 201


@pay.route("/payment_method_type/get/all", methods=["GET"])
def get_all_payment_types():
    np = db.session.query(PaymentMethodTypes).all()

    if np:
        return jsonify(payment_method_types_schema.dump(np)), 200
    else:
        return jsonify("No matching records"), 404


@pay.route("/payment_method_type/add", methods=["POST"])
def pmt_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403

    method_name = post_data.get("method_name")
    method_desc = post_data.get("method_desc")

    if method_name and method_desc:

        new_method_type = PaymentMethodTypes(
            method_name,
            method_desc,
        )
        db.session.add(new_method_type)
        db.session.commit()

        return jsonify(payment_method_schema.dump(new_method_type)), 201
    else:
        return jsonify("Missing critical information for creation"), 403
