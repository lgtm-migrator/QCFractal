"""change server stats collected

Revision ID: 00f7a74dcc37
Revises: e1bfb46d1055
Create Date: 2021-04-25 10:36:07.834628

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "00f7a74dcc37"
down_revision = "e1bfb46d1055"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("server_stats_log", sa.Column("error_count", sa.Integer(), nullable=True))
    op.add_column("server_stats_log", sa.Column("service_queue_status", sa.JSON(), nullable=True))
    op.add_column("server_stats_log", sa.Column("task_queue_status", sa.JSON(), nullable=True))
    op.drop_column("server_stats_log", "result_states")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "server_stats_log",
        sa.Column("result_states", postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    )
    op.drop_column("server_stats_log", "task_queue_status")
    op.drop_column("server_stats_log", "service_queue_status")
    op.drop_column("server_stats_log", "error_count")
    # ### end Alembic commands ###
