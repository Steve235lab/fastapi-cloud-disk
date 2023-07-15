from __future__ import annotations

import os
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session, Query

load_dotenv(override=True)
db_engin = create_engine(os.getenv("POSTGRESQL_DB_URL"))
db_engin.execution_options(schema_translate_map={None: "main"})
Session = scoped_session(sessionmaker(db_engin, autoflush=False))


class BaseModel(declarative_base()):
    __abstract__ = True

    @classmethod
    @property
    def query(cls) -> Query:
        with Session() as session:
            return session.query(cls)

    def add_to_db(self):
        with Session() as session:
            session.add(self)
            session.commit()

    def delete_from_db(self):
        with Session() as session:
            session.delete(self)
            session.commit()

    @classmethod
    def get_by_id(cls, _id: int | UUID | str) -> BaseModel | None:
        """Get record with int ID or UUID"""
        with Session() as session:
            return session.query(cls).get(cls.id == _id)
