import uuid

from sqlalchemy import Column, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from app.DAO.database import BaseModel


class InvitationCode(BaseModel):
    __tablename__ = "invitation_code"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Also the string for user to input.
    storage_size = Column(Integer, nullable=False, default=1024)
    # If a code is not used, this value should be null; else it should be the timestamp when it was used.
    expired_at = Column(Float, nullable=True)
