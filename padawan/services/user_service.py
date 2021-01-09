from typing import Optional

from padawan.data import db_session
from padawan.data.users import User

from passlib.handlers.sha2_crypt import sha512_crypt as crypto


def get_user_count() -> int:
    session = db_session.create_session()
    try:
        return session.query(User).count()
    finally:
        session.close()


def find_user_by_email(email: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        return session.query(User).filter(User.email == email).first()
    finally:
        session.close()


def hash_text(text: str) -> str:
    hashed_text = crypto.encrypt(text, rounds=205206)
    return hashed_text


def create_user(name: str, email: str, password: str) -> Optional[User]:
    if find_user_by_email(email):
        return None

    new_user = User()
    new_user.name = name.strip()
    new_user.email = email.strip().lower()
    new_user.hashed_password = hash_text(password)

    session = db_session.create_session()
    try:
        session.add(new_user)
        session.commit()
    finally:
        session.close()

    return new_user


def verified_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)


def login_user(email: str, password: str) -> Optional[User]:
    session = db_session.create_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            return None

        if not verified_hash(user.hashed_password, password):
            return None

        return user
    finally:
        session.close()


def find_user_by_id(user_id: str) -> Optional[User]:
    session = db_session.create_session()

    try:
        user = session.query(User).filter(User.id == user_id).first()
        return user
    finally:
        session.close()
