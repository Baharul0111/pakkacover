"""Demo encrypted data roots, credentials, consent, usage and adapter records."""
from alembic import op
from apps.api.app.db import Base
revision='001_demo'
down_revision=None
branch_labels=None
depends_on=None
def upgrade():Base.metadata.create_all(bind=op.get_bind())
def downgrade():raise RuntimeError('Destructive demo downgrade is intentionally unavailable')
