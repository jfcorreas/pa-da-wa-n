from typing import Optional, List

from padawan.data import db_session
from padawan.data.redirects import Redirect
from padawan.data.publications import Publication


def get_redirect_count() -> int:
    session = db_session.create_session()
    try:
        return session.query(Redirect).count()
    finally:
        session.close()


def find_redirect_by_id(redirect_id: int) -> Optional[Redirect]:
    session = db_session.create_session()
    try:
        return session.query(Redirect).filter(Redirect.id == redirect_id).first()
    finally:
        session.close()


def get_redirect(short_url: str) -> Optional[Redirect]:
    if not short_url or not short_url.strip():
        return None

    short_url = short_url.strip().lower()

    session = db_session.create_session()

    try:
        return session.query(Redirect).filter(Redirect.short_url == short_url).first()
    finally:
        session.close()


def create_redirect(name: str, short_url: str, url: str, user_email: str) -> Redirect:
    if get_redirect(short_url):
        raise Exception("Cannot create redirect, it already exists!")

    redirect = Redirect()
    redirect.name = name.strip()
    redirect.url = url.strip().lower()
    redirect.short_url = short_url.strip().lower()
    redirect.creating_user = user_email

    session = db_session.create_session()

    try:
        session.add(redirect)
        session.commit()
        return redirect
    finally:
        session.close()


def all_redirects() -> List[Redirect]:
    session = db_session.create_session()

    try:
        return session.query(Redirect).order_by(Redirect.created_date.desc()).all()
    finally:
        session.close()


def find_publication_by_id(publication_id: int) -> Optional[Publication]:
    session = db_session.create_session()
    try:
        return session.query(Publication).filter(Publication.id == publication_id).first()
    finally:
        session.close()
