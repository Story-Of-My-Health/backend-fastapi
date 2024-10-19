from sqlalchemy.orm import Session

from models.user import User
from schemas.user import CreateUserSchema


def create_user(session: Session, user: CreateUserSchema):
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user(session: Session, username: str):
    return session.query(User).filter(User.username == username).one()


def get_user_by_id(session: Session, id: int):
    return session.query(User).filter(User.id == id).one()


def set_user_type(session: Session, id: int, user_type: str):
    user = session.query(User).filter(User.id == id).one()
    user.user_type = user_type
    session.commit()
    return user
