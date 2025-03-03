from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True)
    password = fields.String(load_only=True, required=True)


class GeneratedTextSchema(Schema):
    id = fields.Int(dump_only=True)
    prompt = fields.String(required=True, description="The prompt used for generating text")
    response = fields.String(dump_only=True, description="The generated response")
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)