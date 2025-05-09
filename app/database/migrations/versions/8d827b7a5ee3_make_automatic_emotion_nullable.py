"""make automatic_emotion nullable

Revision ID: 8d827b7a5ee3
Revises: fb8c53d9c5e3
Create Date: 2025-05-10 16:04:20.739259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8d827b7a5ee3'
down_revision: Union[str, None] = 'fb8c53d9c5e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('process_result', 'automatic_emotion',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('process_result', 'automatic_emotion',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.drop_constraint('uix_confusion_matrix', 'confusion_matrix', type_='unique')
    op.drop_constraint('uix_class_metrics', 'class_metrics', type_='unique')
    # ### end Alembic commands ###
