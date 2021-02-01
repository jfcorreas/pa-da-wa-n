import datetime
import sqlalchemy

from padawan.data.modelbase import SqlAlchemyBase


class Publication(SqlAlchemyBase):
    __tablename__ = 'publications'

    id: int = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)

    created_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                                        default=datetime.datetime.now, index=True)
    creating_user: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    updated_date: datetime.datetime = sqlalchemy.Column(sqlalchemy.DateTime,
                                                        default=datetime.datetime.now, index=True)
    updating_user: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    num_reads: int = sqlalchemy.Column(sqlalchemy.Integer, default=0, index=True)

    title: str = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    short_url: str = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    content: str = sqlalchemy.Column(sqlalchemy.String)
    preview: str = sqlalchemy.Column(sqlalchemy.String)
    is_snippet: bool = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
