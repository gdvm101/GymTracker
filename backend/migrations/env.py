from logging.config import fileConfig

from alembic import context

from app.core.config import get_settings
from app.db import models_social  # Register the M/L storage in the same metadata.
from app.db.models import Base
from app.db.session import make_engine


config = context.config
if config.config_file_name and "connection" not in config.attributes:
    fileConfig(config.config_file_name, disable_existing_loggers=False)


def migrate(connection):
    context.configure(connection=connection, target_metadata=Base.metadata, compare_type=True)
    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    context.configure(url=get_settings().database_url, target_metadata=Base.metadata,
                      literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()
elif "connection" in config.attributes:
    migrate(config.attributes["connection"])
else:
    engine = make_engine(get_settings().database_url)
    try:
        with engine.connect() as connection:
            migrate(connection)
    finally:
        engine.dispose()
