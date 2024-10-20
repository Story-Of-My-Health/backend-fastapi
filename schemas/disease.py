from typing import List

from pydantic import BaseModel


class DiseaseSchema(BaseModel):
    id: int
    symptom_signature: str
    disease_name: str


class PredictDiseaseSchema(BaseModel):
    symptoms: List[str]


class PredictDiseaseResponseSchema(BaseModel):
    predicted_disease: str
