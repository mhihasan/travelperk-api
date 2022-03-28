"""create order table

Revision ID: 1964d7f0ab85
Revises: 
Create Date: 2021-07-14 13:08:23.911151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from src.models.order import OrderStatus

revision = "1964d7f0ab85"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "order",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, nullable=False),
        sa.Column("product_code", sa.String, nullable=False),
        sa.Column("customer_fullname", sa.String, nullable=True),
        sa.Column("product_name", sa.String, nullable=True),
        sa.Column("total_amount", sa.Float, default=0),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("status", sa.String, default=OrderStatus.initiated.value),
    )


def downgrade():
    op.drop_table("order")
