"""Add course session and due date to assignments."""
from alembic import op
import sqlalchemy as sa

revision = "0002_assignment_details"
down_revision = "0001_create_tasks"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tasks", sa.Column("session_number", sa.Integer(), nullable=True))
    op.add_column("tasks", sa.Column("due_date", sa.Date(), nullable=True))


def downgrade():
    op.drop_column("tasks", "due_date")
    op.drop_column("tasks", "session_number")
