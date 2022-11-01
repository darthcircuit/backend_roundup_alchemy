from enum import unique
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma
from tables.payment_method_types import *

# from organizations import Organizations, OrganizationsSchema


class PaymentMethods(db.Model):
    __tablename__ = "payment_methods"
    payment_method_id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    account_name = db.Column(db.String(), nullable=False)
    payment_method_type = db.Column(
        db.Integer(), db.ForeignKey("payment_method_types.type_id"), nullable=False
    )
    account_number = db.Column(db.String(), nullable=False, unique=True)
    account_owner_phone = db.Column(db.String(), nullable=False)
    billing_street_address = db.Column(db.String(), nullable=False)
    billing_city = db.Column(db.String(), nullable=False)
    billing_state = db.Column(db.String(), nullable=False)
    billing_postal_code = db.Column(db.String(), nullable=False)
    bank_name = db.Column(db.String(), nullable=False)
    bank_routing_num = db.Column(db.String(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False
    )
    # pay_method = db.relationship("Contributions", back_populates="user_id")

    def __init__(
        self,
        account_name,
        payment_method_type,
        account_number,
        account_owner_phone,
        billing_street_address,
        billing_city,
        billing_state,
        billing_postal_code,
        bank_name,
        active,
    ):
        self.account_name = account_name
        self.payment_method_type = payment_method_type
        self.account_number = account_number
        self.account_owner_phone = account_owner_phone
        self.billing_street_address = billing_street_address
        self.billing_city = billing_city
        self.billing_state = billing_state
        self.billing_postal_code = billing_postal_code
        self.bank_name = bank_name
        self.active = active


class PaymentMethodsSchema(ma.Schema):
    class Meta:
        fields = [
            "payment_method_id",
            "account_name",
            "payment_method",
            "account_number",
            "account_owner_phone",
            "billing_street_address",
            "billing_city",
            "billing_state",
            "billing_postal_code",
            "bank_name",
            "bank_routing_num",
            "active",
            "user_id",
        ]

    payment_method = ma.fields.Nested(PaymentMethodTypesSchema())


payment_method_schema = PaymentMethodsSchema()
payment_methods_schema = PaymentMethodsSchema(many=True)
