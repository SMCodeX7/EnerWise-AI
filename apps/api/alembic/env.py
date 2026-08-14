from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from app.core.config import settings
from app.core.database import Base

# Import all application models so that they are registered
# inside Base.metadata before Alembic performs autogeneration.
import app.models  # noqa: F401


config = context.config


if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Never store the real database URL in alembic.ini.
# Load it from the application's environment configuration instead.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)


target_metadata = Base.metadata


def include_object(
    object_,
    name,
    type_,
    reflected,
    compare_to,
):
    """
    Control which database objects Alembic may manage.

    - Supabase-owned auth tables must never be managed by EnerWise.
    - Existing database tables that are not represented in our
      SQLAlchemy metadata must never be automatically dropped.
    """

    if type_ == "table":
        schema = getattr(object_, "schema", None)

        # Supabase owns the auth schema.
        if schema == "auth":
            return False

        # Prevent Alembic autogenerate from proposing DROP TABLE
        # for database tables that EnerWise does not manage.
        if reflected and compare_to is None:
            return False

    return True


def run_migrations_offline() -> None:
    """Run migrations without creating a live database connection."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_object=include_object,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations using a live database connection."""

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()