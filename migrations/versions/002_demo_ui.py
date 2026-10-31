"""Demo paid time and owner-scoped notifications."""
from alembic import op
import sqlalchemy as sa
from apps.api.app.db import Notification
revision='002_demo_ui'
down_revision='001_demo'
branch_labels=None
depends_on=None
def upgrade():
 bind=op.get_bind()
 if 'paid_at' not in {c['name'] for c in sa.inspect(bind).get_columns('payments',schema='app')}:
  op.add_column('payments',sa.Column('paid_at',sa.DateTime(timezone=True),nullable=True),schema='app')
 Notification.__table__.create(bind,checkfirst=True)
def downgrade():raise RuntimeError('Demo downgrade unavailable')
