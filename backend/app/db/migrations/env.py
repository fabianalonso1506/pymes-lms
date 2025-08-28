import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# No target metadata because we're using explicit migrations
_target_metadata = None

def run_migrations_offline():
    url = os.getenv('DATABASE_URL')
    context.configure(
        url=url,
        target_metadata=_target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    url = os.getenv('DATABASE_URL')
    connectable = engine_from_config(
        {'sqlalchemy.url': url},
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=_target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
