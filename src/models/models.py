from datetime import datetime
from sqlalchemy import String, Column, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(length=128), unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True, nullable=False)
    files = relationship(
        "File",
        back_populates="user",
        passive_deletes=True,
        foreign_keys=[],
    )


class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(128), nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow())
    path = Column(String(128))
    size = Column(Integer)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    is_downloadable = Column(Boolean)
    user = relationship("User", back_populates="files")

    # id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid1)
    # user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    # name = Column(String(125), nullable=False)
    # created_at = Column(DateTime, index=True, default=datetime.utcnow)
    # path = Column(String(255), nullable=False, unique=True)
    # size = Column(Integer, nullable=False)
    # is_downloadable = Column(Boolean, default=False)
