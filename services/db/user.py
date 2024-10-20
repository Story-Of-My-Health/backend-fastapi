from typing import List

from sqlalchemy.orm import Session

from models.user import DoctorProfile, Keyword, User
from schemas.user import CreateUserSchema, DoctorProfileBaseSchema


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


def create_doctor_profile(
    session: Session,
    profile: DoctorProfileBaseSchema,
    user_id: int,
    keywords: List[Keyword],
):
    new_profile = DoctorProfile(
        address=profile.address,
        establishment=profile.establishment,
        keywords=keywords,
        title=profile.title,
        user_id=user_id,
    )
    session.add(new_profile)
    session.commit()
    session.refresh(new_profile)
    return new_profile


def get_doctor_profile_by_id(session: Session, id: int):
    return session.query(DoctorProfile).filter(DoctorProfile.id == id).one()


def get_doctor_profile_by_keyword(session: Session, keywords: List[str]):
    return (
        session.query(DoctorProfile)
        .join(DoctorProfile.keywords)
        .filter(Keyword.name.in_(keywords))
        .all()
    )
