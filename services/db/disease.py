from sqlalchemy.orm import Session

from models.disease import Disease
from schemas.disease import DiseaseSchema


def create_disease(session: Session, disease: DiseaseSchema):
    db_disease = Disease(**disease.model_dump())
    session.add(db_disease)
    session.commit()
    session.refresh(db_disease)
    return db_disease


def get_disease(session: Session, symptom_signature: str):
    return session.query(Disease).filter(Disease.symptom_signature == symptom_signature).one()
