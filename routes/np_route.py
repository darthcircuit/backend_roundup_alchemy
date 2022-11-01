from flask import jsonify, request, Blueprint
from tables.non_prof import NonProfits, NonProfitsSchema, np_schema, nps_schema
from db import db, populate_object


np = Blueprint("np", __name__)


@np.route("/np/get", methods=["GET"])
def get_all_active_np_route():
    np = db.session.query(NonProfits).filter(NonProfits.active == True).all()

    if np:
        return jsonify(nps_schema.dump(np)), 200
    else:
        return jsonify("No matching records"), 404


@np.route("/np/get/<np_id>", methods=["GET"])
def get_np_by_id(np_id):
    np = db.session.query(NonProfits).filter(NonProfits.np_id == np_id).first()

    if np:
        return jsonify(np_schema.dump(np)), 200

    else:
        return jsonify("Invalid"), 404


@np.route("/np/update/<np_id>", methods=["POST"])
def update_np_route(np_id):
    np_ojb = db.session.query(NonProfits).filter(NonProfits.np_id == np_id).first()
    new_data = request.form if request.form else request.json

    if new_data:
        new_data = dict(new_data)
    else:
        return jsonify("No values to change")

    updated_fields = populate_object(np_ojb, new_data)

    if updated_fields:
        db.session.commit()
        return jsonify(f"{', '.join(updated_fields)} updated for np ID: {np_id}")

    else:
        return jsonify(f"No Fields Updated")


@np.route("/np/deactivate/<np_id>", methods=["POST"])
def deactivate_np_route(np_id):
    selected_np = db.session.query(NonProfits).filter(NonProfits.np_id == np_id).first()

    if selected_np:
        selected_np.active = False
        db.session.commit()
        return jsonify(f"np with ID {np_id} has been set to inactive."), 200
    else:
        return "Invalid"


@np.route("/np/activate/<np_id>", methods=["POST"])
def activate_np_route(np_id):
    selected_np = db.session.query(NonProfits).filter(NonProfits.np_id == np_id).first()

    if selected_np:
        selected_np.active = True
        db.session.commit()
        return jsonify(f"np with ID {np_id} has been set to active."), 200
    else:
        return "Invalid"


@np.route("/np/delete/<np_id>", methods=["POST"])
def delete_np_route(np_id):
    selected_np = db.session.query(NonProfits).filter(NonProfits.np_id == np_id).first()

    db.session.delete(selected_np)
    db.session.commit()

    return jsonify(f"np with ID {np_id} has been deleted")


@np.route("/np/add", methods=["POST"])
def np_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403
    name = post_data.get("name")
    address = post_data.get("address")
    city = post_data.get("city")
    state = post_data.get("state")
    phone = post_data.get("phone")
    tax_id = post_data.get("tax_id")

    if name and address and city and state and phone and tax_id:

        new_np = NonProfits(
            name,
            address,
            city,
            state,
            phone,
            tax_id,
        )
        db.session.add(new_np)
        db.session.commit()

        return jsonify("Non Profit Organization created"), 201
    else:
        return jsonify("Missing critical information for creation"), 403
