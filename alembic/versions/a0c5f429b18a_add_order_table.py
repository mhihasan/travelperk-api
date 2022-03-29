"""Add order table

Revision ID: a0c5f429b18a
Revises: 
Create Date: 2022-03-29 10:38:08.669940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0c5f429b18a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "order",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("product_code", sa.String(), nullable=False),
        sa.Column("product_name", sa.String(), nullable=True),
        sa.Column("total_amount", sa.Float(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("order")
    # ### end Alembic commands ###
