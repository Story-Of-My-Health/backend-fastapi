import enum
from typing import Optional

from pydantic import BaseModel


class NotificationAction(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class NotificationModel(enum.Enum):
    IDENTITY = "identity"


class NotificationSchema(BaseModel):
    id: Optional[int] = None
    performer_id: int
    model: str
    action: str
