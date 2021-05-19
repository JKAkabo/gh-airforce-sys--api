from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config


fileConfig(config.config_file_name)

from app.db import Base
# from ..app.db import Base
# from ..app import models
target_metadata = Base.metadata


def get_url():
    user = 'bookmarks'
    passwor = 'edem1234'
    server = 'localhost'
    db = 'airforce'
    return f"postgresql://{user}:{passwor}@{server}/{db}"


def run_migrations_offline():

    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():

    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = engine_from_config(
        # config.get_section(config.config_ini_section),
        configuration,
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
