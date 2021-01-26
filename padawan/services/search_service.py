from typing import List

from padawan.data import db_session
from padawan.data.publications import Publication


def search_publications(query: str) -> List[Publication]:
    session = db_session.create_session()

    try:
        return session.query(Publication).filter(Publication.title.ilike(f"%{query}%"))\
            .order_by(Publication.created_date.desc()).all()
    finally:
        session.close()
