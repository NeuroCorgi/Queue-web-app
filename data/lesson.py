import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import session
from .db_session import SqlAlchemyBase

from data import __all_models as models
from data import db_session as db


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"
     
    id = sqlalchemy.Column("id", sqlalchemy.Integer, autoincrement=True, primary_key=True)

    name = sqlalchemy.Column("name", sqlalchemy.String)
    creator = sqlalchemy.Column("creator", sqlalchemy.ForeignKey("users.id"))

    def __init__(self, name, creator):
        self.name = name
        self.creator = creator

    def get_queue(self):
        session = db.create_session()
        queue = session.query(models.queue.Node).\
                        filter(models.queue.Node.lesson == self.id).\
                        order_by(models.queue.Node.time.asc()).\
                        all()
        queue = [session.query(models.user.User).filter(models.user.User.id == node.user).first().name for node in queue]
        return queue
