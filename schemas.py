from marshmallow import validate, Schema, fields

class UserToSend(Schema):
    id = fields.Integer()
    login = fields.String(validate=validate.Email())
    name = fields.String()

class CreatingUser(Schema):
    login = fields.String(validate=validate.Email())
    psw = fields.String()
    name = fields.String()

class WalletToGet(Schema):
    name = fields.String()
    user_id = fields.Integer()
    currency = fields.String()
    ballance = fields.Integer()

class WalletToSend(Schema):
    id = fields.Integer()
    name = fields.String()
    user_id = fields.Integer()
    currency = fields.String()
    ballance = fields.Integer()

class ValidateTransaction(Schema):
    sender_wallet_id = fields.Integer()
    recevier_wallet_id = fields.Integer()
    amount = fields.Integer()

class ValidateError(Schema):
    code = fields.Integer()
    type = fields.String()
    message = fields.String()