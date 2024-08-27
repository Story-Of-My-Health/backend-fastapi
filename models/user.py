import bcrypt
import jwt
from sqlalchemy import Column, Integer, LargeBinary, String

import settings
from db_initializer import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(LargeBinary, nullable=False, unique=True)
    email = Column(String(225), nullable=True)
    hashed_password = Column(LargeBinary, nullable=False)

    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def validate_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode(), self.hashed_password)

    def generate_token(self) -> dict:
        """Generate access token for user"""
        return {
            "access_token": jwt.encode(
                {"username": self.username, "email": self.email}, settings.SECRET_KEY
            )
        }
