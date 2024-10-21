import enum

import bcrypt
import jwt
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    Table,
    func,
)
from sqlalchemy.orm import relationship

import settings
from db_initializer import Base


class USER_TYPE_CHOICES(enum.Enum):
    regular = "regular"
    doctor = "doctor"
    admin = "admin"


class MEDICAL_HISTORY_STATUS(enum.Enum):
    in_progress = "in_progress"
    success = "success"
    failed = "failed"


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String(225), nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)
    user_type = Column(Enum(USER_TYPE_CHOICES), default=USER_TYPE_CHOICES.regular)
    identity_id = Column(
        Integer,
        ForeignKey("identity.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    identity = relationship("Identity", back_populates="user", uselist=False)
    doctor_profile = relationship("DoctorProfile", back_populates="user", uselist=False)

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


profile_keyword_association = Table(
    "profile_keyword_association",
    Base.metadata,
    Column("profil_id", Integer, ForeignKey("doctor_profile.id", ondelete="CASCADE")),
    Column("keyword_id", Integer, ForeignKey("keyword.id", ondelete="CASCADE")),
)


class DoctorProfile(Base):
    __tablename__ = "doctor_profile"
    id = Column(Integer, nullable=False, primary_key=True)
    title = Column(String(255), nullable=False)
    establishment = Column(String(255), nullable=False)
    address = Column(String(255), nullable=True)
    user_id = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True
    )

    user = relationship("User", back_populates="doctor_profile", uselist=False)
    keywords = relationship(
        "Keyword", secondary=profile_keyword_association, back_populates="profiles"
    )


class Keyword(Base):
    __tablename__ = "keyword"
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)

    profiles = relationship(
        "DoctorProfile",
        secondary=profile_keyword_association,
        back_populates="keywords",
    )


class MedicalHistory(Base):
    __tablename__ = "medical_history"
    id = Column(Integer, nullable=False, primary_key=True)
    symptoms = Column(String(500), nullable=False)
    treatment = Column(String(500), nullable=False)
    disease = Column(String(500), nullable=False)
    status = Column(Enum(MEDICAL_HISTORY_STATUS), nullable=False, default=MEDICAL_HISTORY_STATUS.in_progress)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(
        Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    patient_id = Column(
        Integer, ForeignKey("identity.id", ondelete="CASCADE"), nullable=False
    )

    patient = relationship("Identity", back_populates="medical_history", uselist=False)
