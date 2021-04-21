from marshmallow import Schema, fields
from marshmallow.validate import Range, Length


class MarshReviewSchema(Schema):
    feedback = fields.Str(validate=Length(3, 20))
    grade = fields.Int(validate=Range(1, 100))


