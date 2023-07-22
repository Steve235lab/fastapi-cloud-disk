import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.DAO.database import BaseModel


class SharedFile(BaseModel):
    __tablename__ = "shared_file"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True)
