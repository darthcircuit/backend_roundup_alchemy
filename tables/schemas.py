import marshmallow as ma


class ContributionsSchema(ma.Schema):
    class Meta:
        fields = [
            "user_id",
            "non_profit_id",
            "timestamp",
            "payment_method_id",
            "amount_contributed",
            "roundup_on_off",
        ]


class NonProfitsSchema(ma.Schema):
    class Meta:
        fields = [
            "np_id",
            "name",
            "address",
            "city",
            "state",
            "phone",
            "tax_id",
            # "filing_class",
            "received_contributions",
            "active",
        ]

    received_contributions = ma.fields.Nested(
        ContributionsSchema(),
        exclude=["payment_method_id", "roundup_on_off"],
        many=True,
    )


class PaymentMethodTypesSchema(ma.Schema):
    class Meta:
        fields = ["type_id", "method_name", "method_description"]


class PaymentMethodsSchema(ma.Schema):
    class Meta:
        fields = [
            "payment_method_id",
            "account_name",
            "method_type",
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

    method_type = ma.fields.Nested(PaymentMethodTypesSchema(), exclude=["type_id"])


class UsersSchema(ma.Schema):
    class Meta:
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "mailing_street_address",
            "mailing_city",
            "mailing_state",
            "mailing_postal_code",
            "social_security_num",
            "contributions",
            "active",
            "payment_methods",
            # "supported_non_profs",
        ]

    contributions = ma.fields.Nested(
        ContributionsSchema(), many=True, exclude=["user_id"]
    )
    payment_methods = ma.fields.Nested(
        PaymentMethodsSchema(), many=True, exclude=["user_id"]
    )

    # supported_non_profs = ma.fields.Nested(NonProfitsSchema(), many=True)
    # # except:
    # payment_method = ma.fields.Nested(
    #     PaymentMethodTypesSchema(), exclude=["type_id"]
    # )


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
np_schema = NonProfitsSchema()
nps_schema = NonProfitsSchema(many=True)
payment_method_schema = PaymentMethodsSchema()
payment_methods_schema = PaymentMethodsSchema(many=True)
payment_method_type_schema = PaymentMethodTypesSchema()
payment_method_types_schema = PaymentMethodTypesSchema(many=True)
contribution_schema = ContributionsSchema()
contributions_schema = ContributionsSchema(many=True)
