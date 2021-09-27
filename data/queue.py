from datetime import date, datetime

import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Node(SqlAlchemyBase):
    __tablename__ = "queue"
     
    id = sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True, primary_key=True)
    time = sqlalchemy.Column("time", sqlalchemy.DateTime)
    lesson = sqlalchemy.Column("lesson", sqlalchemy.ForeignKey("lessons.id"))
    user = sqlalchemy.Column("user", sqlalchemy.ForeignKey("users.id"))

    def __init__(self, user, lesson):
        self.lesson = lesson
        self.user = user
        self.time = datetime.now()
