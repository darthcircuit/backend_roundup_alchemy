import uuid
from sqlalchemy.dialects.postgresql import UUID
from db import db

# from organizations import Organizations, OrganizationsSchema


class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.String(), nullable=False, unique=True)
    mailing_street_address = db.Column(db.String(), nullable=False, unique=True)
    mailing_city = db.Column(db.String(), nullable=False)
    mailing_state = db.Column(db.String(), nullable=False)
    mailing_postal_code = db.Column(db.String(), nullable=False)
    social_security_num = db.Column(db.String(), nullable=False, unique=True)
    # org_id = db.Column(
    #     UUID(as_uuid=True), db.ForeignKey("organizations.org_id"), nullable=False
    # )
    active = db.Column(db.Boolean(), nullable=False, default=True)

    payment_methods = db.relationship("PaymentMethods", back_populates="user")
    contributions = db.relationship("Contributions", back_populates="user")
    # supported_non_profs = db.relationship(
    #     "Contributions", secondary="NonProfits", back_populates="user"
    # )

    def __init__(
        self,
        first_name,
        last_name,
        email,
        phone,
        mailing_street_address,
        mailing_city,
        mailing_state,
        mailing_postal_code,
        social_security_num,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.mailing_street_address = mailing_street_address
        self.mailing_city = mailing_city
        self.mailing_state = mailing_state
        self.mailing_postal_code = mailing_postal_code
        self.social_security_num = social_security_num
        self.active = True
