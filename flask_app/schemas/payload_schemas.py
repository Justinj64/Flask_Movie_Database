from marshmallow import (Schema, fields)

'''
    Defining every payload being used in the request as a marshmallow schema
    Validation and restriction of the parameters can be handled here itself
'''


class UserSchema(Schema):
    user_type = fields.Str(required=True)


class TokenSchema(Schema):
    username = fields.Str(required=True)
    token_ttl = fields.Integer(required=True)


class InsertMovieSchema(Schema):
    name = fields.Str(required=True)
    popularity = fields.Float(default=0.0)
    director = fields.Str(required=True)
    imdb_score = fields.Float(default=0)
    genres = fields.List(fields.Str(), required=True)


class UpdateMovieSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str()
    popularity = fields.Float()
    director = fields.Str()
    imdb_score = fields.Float()
    genres = fields.List(fields.Str())


class DeleteMovieSchema(Schema):
    id = fields.Int(required=True)
