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
