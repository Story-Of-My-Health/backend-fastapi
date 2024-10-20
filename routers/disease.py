from typing import Callable, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

from db_initializer import get_db
from models.identity import SEXE_CHOICES, STATUS_CHOICES
from notifications import notify_client
from schemas.disease import PredictDiseaseResponseSchema, PredictDiseaseSchema
from schemas.identity import (CreateIdentitySchema, IdentityQuerySchema,
                              IdentitySchema, UpdateIdentitySchema)
from schemas.notification import (NotificationAction, NotificationModel,
                                  NotificationSchema)
from services.db import identity as identity_db_services

router = APIRouter(prefix="/identity", tags=["identity"])


@router.post("/disease/predict", response_model=PredictDiseaseResponseSchema)
async def predict_disease(
    payload: PredictDiseaseSchema = Body(), session: Session = Depends(get_db)
):

    pass
