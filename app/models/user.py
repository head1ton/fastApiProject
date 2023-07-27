from typing import TYPE_CHECKING

from sqlalchemy import Column, BigInteger, String, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


if TYPE_CHECKING:
    from .item import Item


class User(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    items = relationship("Item", back_populates="owner")
