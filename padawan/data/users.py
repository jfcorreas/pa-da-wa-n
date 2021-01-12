import datetime
import sqlalchemy

from padawan.data.modelbase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                                        default=datetime.datetime.now, index=True)

    name: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email: str = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    # TODO profile_image_url = sqlalchemy.Column(sqlalchemy.String)
    last_login: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                                      default=datetime.datetime.now, index=True)
    is_admin: bool = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
