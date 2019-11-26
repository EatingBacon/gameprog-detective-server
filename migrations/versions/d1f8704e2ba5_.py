"""empty message

Revision ID: d1f8704e2ba5
Revises: 
Create Date: 2019-11-26 16:25:56.569634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1f8704e2ba5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('telegram_handle', sa.String(length=64), nullable=True),
    sa.Column('telegram_start_token', sa.String(length=64), nullable=False),
    sa.Column('current_story_point', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('current_story_point'),
    sa.UniqueConstraint('telegram_handle')
    )
    op.create_table('contact',
    sa.Column('contact_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('firstname', sa.String(length=64), nullable=True),
    sa.Column('lastname', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('contact_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('contact')
    op.drop_table('user')
    # ### end Alembic commands ###