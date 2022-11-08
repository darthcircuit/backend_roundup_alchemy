from flask import jsonify, request, Blueprint
from tables.non_prof import NonProfits
from db import db, populate_object
from tables.schemas import np_schema, nps_schema


np = Blueprint("np", __name__)


@np.route("/np/get/all", methods=["GET"])
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

    required_fields = ["name", "address", "city", "state", "phone", "tax_id"]
    post_data = dict(post_data)
    missing_fields = []
    for field in required_fields:
        if field not in post_data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify(f"{missing_fields} not found"), 404

    new_np = NonProfits(
        post_data["name"],
        post_data["address"],
        post_data["city"],
        post_data["state"],
        post_data["phone"],
        post_data["tax_id"],
    )

    db.session.add(new_np)
    db.session.commit()

    return jsonify("Non Profit Organization created"), 201
