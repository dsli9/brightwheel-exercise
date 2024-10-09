import logging
from pathlib import Path
import urllib.parse

from sqlalchemy import (
    Engine,
    create_engine,
)
from yoyo import get_backend, read_migrations


logger = logging.getLogger(__name__)

# In the real world, DB credentials should be NOT be defined here but I'm just putting them
# here given that this is an exercise with a time constraint.
DB_HOST = "localhost"
DB_USER = "brightwheel-user"
DB_PWD = "brightwheel-password"
DB_DATABASE = "brightwheel-dev-db"
DB_PORT = 52601


MIGRATIONS_DIR = Path(__file__).parents[0] / "schema_migrations"


def get_database_url(redacted: bool = False) -> str:
    pwd = urllib.parse.quote(DB_PWD, safe="")
    logger.debug(
        f"Using database URL: postgresql://{DB_USER}:{'<REDACTED>' if redacted else pwd}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}",
    )
    return f"postgresql://{DB_USER}:{pwd}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"


def create_database_engine() -> Engine:
    engine = create_engine(get_database_url(), pool_pre_ping=True)
    return engine


def migrate_database(
    database: Engine, migrations_path: str | Path = MIGRATIONS_DIR
) -> None:
    logger.info("Running database migrations")
    backend = get_backend(database.url.render_as_string(hide_password=False))
    with backend.lock():
        migrations = read_migrations(str(migrations_path))
        backend.apply_migrations(backend.to_apply(migrations))
