import enum

import bcrypt
import jwt
from sqlalchemy import Column, Enum, ForeignKey, Integer, LargeBinary, String
from sqlalchemy.orm import relationship

import settings
from db_initializer import Base


class USER_TYPE_CHOICES(enum.Enum):
    regular = "regular"
    doctor = "doctor"
    admin = "admin"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String(225), nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)
    user_type = Column(Enum(USER_TYPE_CHOICES), default=USER_TYPE_CHOICES.regular)
    identity_id = Column(
        Integer, ForeignKey("identity.id"), nullable=False, unique=True
    )

    identity = relationship("Identity", back_populates="user", uselist=False)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {
                    "id": self.id,
                    "username": self.username,
                    "email": self.email,
                    "user_type": self.user_type.value,
                    "identity_id": self.identity_id,
                },
                settings.SECRET_KEY,
            )
        }


class DoctorProfile(Base):
    __tablename__ = "doctor_profile"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(255), nullable=False)
    establishment = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    keywords = Column(String(255), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
