import datetime
import markdown
from typing import Optional, List

from padawan.data import db_session
from padawan.data.redirects import Redirect
from padawan.data.publications import Publication


def convert_to_html(md_text) -> str:
    config = {
        'extra': {
            'footnotes': {
                'UNIQUE_IDS': True
            },
            'fenced-code': {
                'lang-prefix': 'lang-'
            }
        },
        'toc': {
            'permalink': True
        }
    }
    extensions = [
        'codehilite',
        'extra'
    ]
    return markdown.markdown(md_text, extensions=extensions, extension_configs=config)


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


def update_redirect(redirect_id: int, name: str, short_url: str, url: str) -> Redirect:
    session = db_session.create_session()

    try:
        redirect = session.query(Redirect).filter(Redirect.id == redirect_id).first()
        if not redirect:
            raise Exception(f"Cannot update redirect: {short_url}, it does not exists!")
        redirect.name = name
        redirect.short_url = short_url
        redirect.url = url
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


def all_publications() -> List[Publication]:
    session = db_session.create_session()

    try:
        return session.query(Publication).order_by(Publication.created_date.desc()).all()
    finally:
        session.close()


def get_publication_by_url(short_url: str) -> Optional[Publication]:
    session = db_session.create_session()
    try:
        return session.query(Publication).filter(Publication.short_url == short_url).first()
    finally:
        session.close()


def create_publication(title: str, short_url: str, content: str, is_snippet: bool, user_email: str) -> Redirect:
    if get_redirect(short_url):
        raise Exception("Cannot create redirect, it already exists!")

    publication = Publication()
    publication.title = title.strip()
    publication.content = content.strip()
    publication.preview = convert_to_html(publication.content[0:800])
    publication.short_url = None
    if short_url:
        publication.short_url = short_url.strip().lower()
    publication.is_snippet = is_snippet
    publication.creating_user = user_email
    publication.updating_user = user_email

    session = db_session.create_session()

    try:
        session.add(publication)
        session.commit()
        return publication
    finally:
        session.close()


def update_publication(publication_id: int, title: str, short_url: str, content: str, is_snippet: bool, user_email: str) -> Redirect:
    session = db_session.create_session()

    try:
        publication = session.query(Publication).filter(Publication.id == publication_id).first()
        if not publication:
            raise Exception(f"Cannot update publication: {title}, it does not exists!")
        publication.title = title.strip()
        publication.short_url = None
        if short_url:
            publication.short_url = short_url.strip().lower()
        publication.content = content.strip()
        publication.preview = convert_to_html(publication.content[0:800])
        publication.is_snippet = is_snippet
        publication.updating_user = user_email
        publication.updated_date = datetime.datetime.now()
        session.commit()
        return publication
    finally:
        session.close()


def get_snippet_content(snippet_url: str) -> Optional[str]:
    session = db_session.create_session()

    try:
        snippet: Publication = session.query(Publication).\
                    filter(Publication.is_snippet == True).\
                    filter(Publication.short_url == snippet_url).first()
    finally:
        session.close()
    if snippet:
        return snippet.content
    return None
