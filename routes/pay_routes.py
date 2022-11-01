from flask import jsonify, request, Blueprint
from tables import payment_methods
from tables.payment_methods import (
    PaymentMethods,
    PaymentMethodsSchema,
    payment_methods_schema,
)
from tables.payment_method_types import (
    PaymentMethodTypes,
    PaymentMethodTypesSchema,
    payment_method_types_schema,
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

    account_name = post_data.get("account_name")
    payment_method_type = post_data.get("payment_method_type")
    account_number = post_data.get("account_number")
    account_owner_phone = post_data.get("account_owner_phone")
    billing_street_address = post_data.get("billing_street_address")
    billing_city = post_data.get("billing_city")
    billing_state = post_data.get("billing_state")
    billing_postal_code = post_data.get("billing_postal_code")
    bank_name = post_data.get("bank_name")

    if (
        account_name
        and payment_method_type
        and account_number
        and account_owner_phone
        and billing_street_address
        and billing_city
        and billing_postal_code
        and billing_state
        and bank_name
    ):

        new_method = PaymentMethods(
            account_name,
            payment_method_type,
            account_number,
            account_owner_phone,
            billing_street_address,
            billing_city,
            billing_state,
            billing_postal_code,
            bank_name,
        )
        db.session.add(new_method)
        db.session.commit()

        return jsonify("Payment method added"), 201
    else:
        return jsonify("Missing critical information for creation"), 403


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

        return jsonify("Added Payment method type"), 201
    else:
        return jsonify("Missing critical information for creation"), 403
