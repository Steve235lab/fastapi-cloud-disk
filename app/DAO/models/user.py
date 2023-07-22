from __future__ import annotations

import time
import uuid

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from app.DAO.database import BaseModel, Session


class User(BaseModel):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    storage_size = Column(Integer, default=1024, nullable=False)  # Unit: MB
    last_seen = Column(Float, default=0.0, nullable=False)  # Timestamp of last login
    login_counter = Column(Integer, default=0, nullable=False)

    def touch(self, name: str | None = None, email: str | None = None):
        with Session() as session:
            if name is not None:
                self.name = name
            if email is not None:
                self.email = email
            self.last_seen = time.time()
            self.login_counter += 1
            session.commit()

    @classmethod
    def get_by_name(cls, name: str) -> User | None:
        with Session() as session:
            return session.query(cls).filter(cls.name == name).one_or_none()
