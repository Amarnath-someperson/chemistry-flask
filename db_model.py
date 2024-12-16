from enum import unique
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reactant = db.Column(db.String, nullable=False)
    product = db.Column(db.String, nullable=False)
    reactant_type = db.Column(db.String, nullable=False)
    product_type = db.Column(db.String, nullable=False)
    catalyst = db.Column(db.String, nullable=True)
    spc_name = db.Column(db.String, nullable=False, unique=True)
    significance = db.Column(db.String, nullable=True)
    description = db.Column(db.Text, nullable=True)
