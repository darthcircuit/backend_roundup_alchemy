from flask import jsonify, request, Blueprint
from tables.users import Users
from tables.schemas import user_schema, users_schema
from db import db, populate_object


users = Blueprint("users", __name__)


@users.route("/users/get", methods=["GET"])
def get_all_active_users_route():
    users = db.session.query(Users).filter(Users.active == True).all()

    if users:
        return jsonify(users_schema.dump(users)), 200
    else:
        return jsonify("No matching records"), 404


@users.route("/user/get/<user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if user:
        return jsonify(user_schema.dump(user)), 200

    else:
        return jsonify("Invalid Organizaion"), 404


@users.route("/user/update/<user_id>", methods=["POST"])
def update_user_route(user_id):
    user_ojb = db.session.query(Users).filter(Users.user_id == user_id).first()
    new_data = request.form if request.form else request.json

    if new_data:
        new_data = dict(new_data)
    else:
        return jsonify("No values to change")

    updated_fields = populate_object(user_ojb, new_data)

    if updated_fields:
        db.session.commit()
        return jsonify(user_schema.dump(user_ojb))

    else:
        return jsonify(f"No Fields Updated")


@users.route("/user/deactivate/<user_id>", methods=["POST"])
def deactivate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = False
        db.session.commit()
        return jsonify(user_schema.dump(selected_user)), 200
    else:
        return "Invalid"


@users.route("/user/activate/<user_id>", methods=["POST"])
def activate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = True
        db.session.commit()
        return jsonify(user_schema.dump(selected_user)), 200
    else:
        return "Invalid"


@users.route("/user/delete/<user_id>", methods=["POST"])
def delete_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    db.session.delete(selected_user)
    db.session.commit()

    return jsonify(user_schema.dump(selected_user))


@users.route("/user/add", methods=["POST"])
def user_add():
    post_data = request.form if request.form else request.json
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "mailing_street_address",
        "mailing_city",
        "mailing_state",
        "mailing_postal_code",
        "social_security_num",
    ]
    if not post_data:
        return jsonify("No data recieved"), 403

    post_data = dict(post_data)
    missing_fields = []
    for field in required_fields:
        if field not in post_data:
            missing_fields.append(field)

    if missing_fields:
        return jsonify(f"{missing_fields} not found"), 404

    new_user = Users(
        post_data["first_name"],
        post_data["last_name"],
        post_data["email"],
        post_data["phone"],
        post_data["mailing_street_address"],
        post_data["mailing_city"],
        post_data["mailing_state"],
        post_data["mailing_postal_code"],
        post_data["social_security_num"],
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user)), 201
