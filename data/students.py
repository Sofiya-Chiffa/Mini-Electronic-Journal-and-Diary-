import sqlalchemy
from .db_session import ORMBase


class Students(ORMBase):
    __tablename__ = 'students'

    s_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    otchestvo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
