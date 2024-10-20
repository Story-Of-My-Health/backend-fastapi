import enum
import hashlib
import json

from sqlalchemy import Column, Integer, String

from db_initializer import Base


class Disease(Base):
    __tablename__ = "disease"
    id = Column(Integer, nullable=False, primary_key=True)
    symptom_signature = Column(String, nullable=False, unique=True)
    disease_name = Column(String(255), nullable=False)

    @staticmethod
    def generate_signature(sample):
        json_string = json.dumps(sample)
        signature = hashlib.sha256(json_string.encode()).hexdigest()
        return signature
