import sqlalchemy
from .db_session import ORMBase


class Classes(ORMBase):
    __tablename__ = 'classes'

    cl_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    number = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    letter = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    schedule = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    time_schedule = sqlalchemy.Column(sqlalchemy.String, nullable=True)
