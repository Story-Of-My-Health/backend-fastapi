from sqlalchemy.orm import Session

from models.identity import Identity
from schemas.identity import CreateIdentitySchema


def create_identity(session: Session, identity: CreateIdentitySchema):
    db_identity = Identity(**identity.model_dump())
    db_identity.identity_key = Identity.generate_identity_id()
    session.add(db_identity)
    session.commit()
    session.refresh(db_identity)
    return db_identity


def get_identities(session: Session):
    return session.query(Identity).all()


def get_identity_by_id(session: Session, id: int):
    return session.query(Identity).filter(Identity.id == id).one()


def get_identity_by_key(session: Session, key: str):
    return session.query(Identity).filter(Identity.identity_key == key).one()
