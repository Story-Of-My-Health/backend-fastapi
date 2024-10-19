import enum
import random
import string

from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db_initializer import Base


class SEXE_CHOICES(enum.Enum):
    male = "male"
    female = "female"


class STATUS_CHOICES(enum.Enum):
    pending = "pending"
    rejected = "rejected"
    done = "done"


class Identity(Base):
    __tablename__ = "identity"
    id = Column(Integer, nullable=False, primary_key=True)
    identity_key = Column(String(20), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=True)
    birth_date = Column(Date, nullable=False)
    birth_place = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    sexe = Column(Enum(SEXE_CHOICES), nullable=False, default=SEXE_CHOICES.male)
    distinctive_trait = Column(String(255), nullable=True)
    profession = Column(String(255), nullable=True)
    status = Column(
        Enum(STATUS_CHOICES), nullable=False, default=STATUS_CHOICES.pending
    )
    father_id = Column(
        Integer, ForeignKey("identity.id", ondelete="SET NULL"), nullable=True
    )
    mother_id = Column(
        Integer, ForeignKey("identity.id", ondelete="SET NULL"), nullable=True
    )

    user = relationship("User", back_populates="identity", uselist=False)

    @staticmethod
    def generate_identity_id(length=12):
        chars = string.ascii_uppercase + string.digits
        id = "".join(random.choice(chars) for _ in range(length))
        return id
