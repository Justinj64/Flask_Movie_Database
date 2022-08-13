# Import Modules:

from marshmallow import (Schema, fields)


class UserSchema(Schema):
    user_type = fields.Str(required=True)


class TokenSchema(Schema):
    username = fields.Str(required=True)
    token_ttl = fields.Integer(required=True)