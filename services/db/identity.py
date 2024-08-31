from sqlalchemy.orm import Session
from sqlalchemy import exc

from models.identity import STATUS_CHOICES, Identity
from schemas.identity import CreateIdentitySchema, IdentityQuerySchema


def create_identity(session: Session, identity: CreateIdentitySchema):
    db_identity = Identity(**identity.model_dump())
    db_identity.identity_key = Identity.generate_identity_id()
    session.add(db_identity)
    session.commit()
    session.refresh(db_identity)
    return db_identity


def get_identities(session: Session, query: IdentityQuerySchema):
    query_dict = query.model_dump()
    filter = {k: v for k, v in query_dict.items() if v}
    return session.query(Identity).filter_by(**filter).all()


def get_identity_by_id(session: Session, id: int):
    return session.query(Identity).filter(Identity.id == id).one()


def get_identity_by_key(session: Session, key: str):
    return session.query(Identity).filter(Identity.identity_key == key).one()


def set_identity_status(
    session: Session,
    id: int,
    status: STATUS_CHOICES,
):
    identity = session.query(Identity).filter(Identity.id == id).one()
    if identity.status != STATUS_CHOICES.pending:
        raise exc.InvalidRequestError
    identity.status = status
    session.commit()
    return identity
