import sqlalchemy
from .db_session import ORMBase
import sqlalchemy.orm as orm


class Teachers(ORMBase):
    __tablename__ = 'teachers'

    t_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    otchestvo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    login = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    cls = orm.relation('Classes', back_populates='teachers')
