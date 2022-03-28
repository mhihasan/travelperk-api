"""create product table

Revision ID: f7544b394e7d
Revises: 1964d7f0ab85
Create Date: 2021-07-14 07:27:22.667892

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f7544b394e7d"
down_revision = "1964d7f0ab85"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "product",
        sa.Column("code", sa.String, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("price", sa.Float, nullable=False),
    )


def downgrade():
    op.drop_table("product")
