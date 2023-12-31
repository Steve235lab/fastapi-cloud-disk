import uuid

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from app.DAO.database import BaseModel


class File(BaseModel):
    __tablename__ = "file"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String, nullable=False)
    download_cnt = Column(Integer, nullable=False, default=0)
