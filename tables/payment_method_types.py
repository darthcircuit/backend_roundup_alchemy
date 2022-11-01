from enum import unique
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

# from organizations import Organizations, OrganizationsSchema


class PaymentMethodTypes(db.Model):
    __tablename__ = "payment_method_types"
    type_id = db.Column(db.Integer(), db.Identity(start=1), primary_key=True)
    method_name = db.Column(db.String(), nullable=False)
    method_description = db.Column(db.String(), nullable=False)

    def __init__(self, method_name, method_description):
        self.method_name = method_name
        self.method_description = method_description


class PaymentMethodTypesSchema(ma.Schema):
    class Meta:
        fields = ["type_id", "method_name", "method_description"]

    # organization = ma.fields.Nested(OrganizationsSchema())


payment_method_type_schema = PaymentMethodTypesSchema()
payment_method_types_schema = PaymentMethodTypesSchema(many=True)
