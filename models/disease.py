import hashlib
import json
from typing import Dict, List

import numpy as np
from sqlalchemy import Column, Integer, String

from db_initializer import Base
from utils.constants import SYMPTOMS_LIST, SYMPTOMS_SAMPLE


class Disease(Base):
    __tablename__ = "disease"
    id = Column(Integer, nullable=False, primary_key=True)
    symptom_signature = Column(String, nullable=False, unique=True)
    disease_name = Column(String(255), nullable=False)

    @staticmethod
    def generate_signature(sample):
        json_string = json.dumps(sample)
        return hashlib.sha256(json_string.encode()).hexdigest()

    @staticmethod
    def create_sample_symptom(symptoms: List[str]) -> Dict[str, int]:
        sample_data = SYMPTOMS_SAMPLE.copy()
        for symptom in symptoms:
            if symptom in np.array(SYMPTOMS_LIST):
                sample_data[symptom] = 1

        return sample_data
