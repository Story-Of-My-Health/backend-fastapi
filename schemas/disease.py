from typing import List

from pydantic import BaseModel, field_validator

from utils.constants import SYMPTOMS_LIST


class DiseaseBaseSchema(BaseModel):
    symptom_signature: str
    disease_name: str


class DiseaseSchema(DiseaseBaseSchema):
    id: int


class SymptomSchema(BaseModel):
    symptoms: List[str]

    @field_validator("symptoms", mode="before")
    def check_symptoms(cls, symptoms):
        for symptom in symptoms:
            if symptom not in SYMPTOMS_LIST:
                raise ValueError(f"{symptom} not in {SYMPTOMS_LIST}")
        return symptoms
