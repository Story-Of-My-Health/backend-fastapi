from fastapi import APIRouter, Body, Depends
from sqlalchemy import exc
from sqlalchemy.orm import Session

from core.prediction import prediction_wrapper
from db_initializer import get_db
from models.disease import Disease
from schemas.disease import DiseaseBaseSchema, DiseaseSchema, SymptomSchema
from services.db import disease as disease_service
from utils.constants import SYMPTOMS_LIST

router = APIRouter(prefix="/disease", tags=["Disease"])


@router.post("/predict", response_model=DiseaseSchema)
async def predict_disease(
    payload: SymptomSchema = Body(), session: Session = Depends(get_db)
):
    # symptoms = Disease.create_sample_symptom(payload.symptoms)
    # print("symproms =>")
    # print(symptoms)

    symptom_signature = Disease.generate_signature(payload.symptoms)

    try:
        db_disease = disease_service.get_disease(session, symptom_signature)
    except exc.NoResultFound:
        disease_name = prediction_wrapper(payload.symptoms)
        db_disease = disease_service.create_disease(
            session,
            DiseaseBaseSchema(
                disease_name=disease_name, symptom_signature=symptom_signature
            ),
        )

    return db_disease


@router.get("/symptoms/", response_model=SymptomSchema)
def get_symptom_list():
    return SymptomSchema(symptoms=SYMPTOMS_LIST)
