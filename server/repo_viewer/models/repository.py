from .base import db
from .base import ma

from marshmallow import fields


class Repository(db.Model):
    __tablename__ = 'repository'
    id = db.Column(db.Integer, primary_key=True)
    github_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)  # length?
    created_date = db.Column(db.Date, nullable=False)
    last_push_date = db.Column(db.Date)  # nullable? what if it's a new repo?
    description = db.Column(db.String)  # nullable? length?
    num_stars = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Repository: '{}' ({}), url: {}>".format(
            self.id,
            self.github_id,
            self.url
        )


class RepositorySchema(ma.Schema):
    id = fields.Integer()
    github_id = fields.Integer()
    name = fields.String()
    url = fields.String()
    created_date = fields.Date()
    last_push_date = fields.Date()
    description = fields.String()
    num_stars = fields.Integer()


repository_schema = RepositorySchema()
repositories_schema = RepositorySchema(many=True)
