import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase

from flask_login.mixins import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = "users"
     
    id = sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True, primary_key=True)
    
    name = sqlalchemy.Column("name", sqlalchemy.String)
    saxion_id = sqlalchemy.Column("saxion_id", sqlalchemy.Integer)

    def __init__(self, name, saxion_id):
        self.name = name
        self.saxion_id = saxion_id
