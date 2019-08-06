from dynaconf import settings
from playhouse.pool import PooledPostgresqlExtDatabase

database = PooledPostgresqlExtDatabase(
    settings['PG_DB'],
    max_connections=32,
    stale_timeout=30,
    user=settings['PG_USER'],
    host=settings['PG_HOST'],
    password=settings['PG_PASSWORD'],
    register_hstore=False
)
