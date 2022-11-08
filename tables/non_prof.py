import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db
import marshmallow as ma


class NonProfits(db.Model):
    __tablename__ = "non_profits"
    np_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    address = db.Column(db.String())
    city = db.Column(db.String())
    state = db.Column(db.String())
    phone = db.Column(db.String(), nullable=False, unique=True)
    tax_id = db.Column(db.String(), nullable=False, unique=True)
    #    filing_class = db.Column(db.Integer())
    # org_id = db.Column(
    #     UUID(as_uuid=True), db.ForeignKey("organizations.org_id"), nullable=False
    # )
    active = db.Column(db.Boolean(), default=True)
    received_contributions = db.relationship("Contributions", back_populates="np")
    # user = db.relationship(
    #     "Contributions", secondary="Users", back_populates="supported_non_profs"
    # )

    def __init__(self, name, address, city, state, phone, tax_id):
        self.name = name
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone
        self.tax_id = tax_id
        # self.filing_class = filing_class
        self.active = True
