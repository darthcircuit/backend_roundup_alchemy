from flask import jsonify, request, Blueprint
from tables.users import Users, user_schema, users_schema
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
        return jsonify(f"{', '.join(updated_fields)} updated for User ID: {user_id}")

    else:
        return jsonify(f"No Fields Updated")


@users.route("/user/deactivate/<user_id>", methods=["POST"])
def deactivate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = False
        db.session.commit()
        return jsonify(f"User with ID {user_id} has been set to inactive."), 200
    else:
        return "Invalid"


@users.route("/user/activate/<user_id>", methods=["POST"])
def activate_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    if selected_user:
        selected_user.active = True
        db.session.commit()
        return jsonify(f"User with ID {user_id} has been set to active."), 200
    else:
        return "Invalid"


@users.route("/user/delete/<user_id>", methods=["POST"])
def delete_user_route(user_id):
    selected_user = db.session.query(Users).filter(Users.user_id == user_id).first()

    db.session.delete(selected_user)
    db.session.commit()

    return jsonify(f"User with ID {user_id} has been deleted")


@users.route("/user/add", methods=["POST"])
def user_add():
    post_data = request.form if request.form else request.json

    if not post_data:
        return jsonify("No data recieved"), 403
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    email = post_data.get("email")
    phone = post_data.get("phone")
    street_address = post_data.get("mailing_street_address")
    city = post_data.get("mailing_city")
    state = post_data.get("mailing_state")
    postal_code = post_data.get("mailing_postal_code")
    ssn = post_data.get("social_security_num")

    if (
        first_name
        and last_name
        and email
        and phone
        and street_address
        and city
        and state
        and postal_code
        and ssn
    ):

        new_user = Users(
            first_name,
            last_name,
            email,
            phone,
            street_address,
            city,
            state,
            postal_code,
            ssn,
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify("User created"), 201
    else:
        return jsonify("Missing critical information for user creation"), 403
