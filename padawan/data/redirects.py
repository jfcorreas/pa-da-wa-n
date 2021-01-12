import datetime
import sqlalchemy

from padawan.data.modelbase import SqlAlchemyBase


class Redirect(SqlAlchemyBase):
    __tablename__ = 'redirects'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                                        default=datetime.datetime.now, index=True)
    creating_user: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    short_url: str = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    name: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    url: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)

