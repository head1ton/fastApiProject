from typing import TYPE_CHECKING

from sqlalchemy import Column, BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..db.base_class import Base

if TYPE_CHECKING:
    from .user import User


class Item(Base):
    id = Column(BigInteger, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="items")
