from logging.config import fileConfig

from sqlalchemy import engine_from_config, create_engine
from sqlalchemy import pool

from alembic import context
import os
import sys
import dotenv

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import app.DAO.models
from app.DAO.database import BaseModel

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
schema = "main"

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

dotenv.load_dotenv(override=True)
config.set_main_option("sqlalchemy.url", os.environ.get("POSTGRESQL_DB_URL"))
print(config.get_main_option("sqlalchemy.url"))

target_metadata = BaseModel.metadata

include_table_names = [
    "file",
    "invitation_code",
    "shared_file",
    "user",
]


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and name not in include_table_names:
        return False
    return True


def include_name(name, type_, parent_name):
    """Set which schema to operate in config"""
    print("include name: ", type_, name, parent_name)
    if type_ == "schema":
        return name in ["perception"]
    else:
        return True


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    print("run_migrations_offline")
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_object=include_object,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        # include_schemas=True,
        # include_name=include_name,
    )

    with context.begin_transaction():
        # context.execute("SET search_path TO perception")  # set which schema to operate, default="public"
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # print(f"run_migrations_online, meta_data: {target_metadata.tables}")
    engine = create_engine(
        url=config.get_main_option("sqlalchemy.url"), connect_args={"options": f"-csearch_path={schema}"}
    )
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            # include_schemas=True,
            # include_name=include_name,
        )

        with context.begin_transaction():
            # context.execute("SET search_path TO perception")  # set which schema to operate, default="public"
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
