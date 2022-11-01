from enum import unique
import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma

# from tables.non_prof import NonProfits, NonProfitsSchema
from datetime import datetime

# from organizations import Organizations, OrganizationsSchema


class Contributions(db.Model):
    __tablename__ = "contributions"
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.user_id"),
        primary_key=True,
        nullable=False,
    )
    np_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("non_profits.np_id"),
        primary_key=True,
        nullable=False,
    )
    timestamp = db.Column(
        db.DateTime(), primary_key=True, nullable=False, default=datetime.now()
    )

    payment_method_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("payment_methods.payment_method_id"),
        nullable=False,
    )
    amount_contributed = db.Column(db.Float(), nullable=False)
    roundup_on_off = db.Column(db.Boolean(), default=False)

    def __init__(
        self,
        user_id,
        non_profit_id,
        payment_method_id,
        amount_contributed,
        roundup_on_off,
    ):
        self.user_id = user_id
        self.payment_method_id = payment_method_id
        self.non_profit_id = non_profit_id
        self.amount_contributed = amount_contributed
        self.timestamp = datetime.now()
        self.roundup_on_off = roundup_on_off


class ContributionsSchema(ma.Schema):
    class Meta:
        fields = [
            "user_id",
            "non_profit_id",
            "timestamp",
            "payment_method_id",
            "amount_contributed",
            "roundup_on_off",
            # "non_prof",
        ]

    # non_prof = ma.fields.Nested(NonProfitsSchema())


contribution_schema = ContributionsSchema()
contributions_schema = ContributionsSchema(many=True)
