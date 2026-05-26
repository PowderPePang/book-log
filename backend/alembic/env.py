from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import sys
import os

from dotenv import load_dotenv

# This tells Python to look in your root folder so it can find the 'backend' module.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(os.path.dirname(BASE_DIR))

# We tell dotenv exactly where the .env file is located (backend/.env)
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Import the Base master catalog
from app.db.base import Base

# CRITICAL: You MUST import your models here, even if you don't use them directly. 
# If they are not imported, Base.metadata will be empty, and Alembic won't see them.
from app.models.user import User
from app.models.book import Book

# os.getenv safely retrieves the value from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")
# If it can't find the URL in the .env file, crash immediately with a helpful error.
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file!")

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# this tells Alembic to borrow the exact same connection URL that your application uses in session.py
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
