from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool, text
from alembic import context
from app.config import settings
from app.db import Base
from app import models

config = context.config
config.set_main_option("sqlalchemy.url", settings.database_url)
if config.config_file_name:
    fileConfig(config.config_file_name)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(url=settings.database_url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        # Serialize migrations when multiple Kubernetes replicas start together.
        postgres = connection.dialect.name == "postgresql"
        if postgres:
            connection.execute(text("SELECT pg_advisory_lock(210021)"))
            connection.commit()
        try:
            context.configure(connection=connection, target_metadata=target_metadata)
            with context.begin_transaction():
                context.run_migrations()
        finally:
            if postgres:
                connection.execute(text("SELECT pg_advisory_unlock(210021)"))
                connection.commit()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
