from logging.config import fileConfig

from alembic import context
from core.config import SQLALCHEMY_DATABASE_URI
from core.db.models import Base
from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Override sqlalchemy.url with the one from config.py
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URI)

# Configure logging (if a config file is specified)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set SQLAlchemy metadata object for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations() -> None:
    """Run migrations using SQLAlchemy engine configuration."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


run_migrations()
