import asyncio
from alembic import context
from apps.api.app.db import Base,engine

def run(connection):
 context.configure(connection=connection,target_metadata=Base.metadata,version_table_schema='app')
 with context.begin_transaction():context.run_migrations()
async def online():
 async with engine.begin() as c:
  await c.exec_driver_sql('CREATE SCHEMA IF NOT EXISTS app')
 async with engine.connect() as c:await c.run_sync(run)
 await engine.dispose()
asyncio.run(online())
