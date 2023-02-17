"""empty message

Revision ID: df60487c3cd2
Revises: 5e811a998c9c
Create Date: 2023-02-17 20:44:01.402845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df60487c3cd2'
down_revision = '5e811a998c9c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('planet_from', sa.String(length=120), nullable=False),
    sa.Column('birth_year', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('planet_from')
    )
    op.create_table('planets',
    sa.Column('planet_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('diameter', sa.Integer(), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.Column('climate', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('planet_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('vehicles',
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('vehicle_id', sa.Integer(), nullable=False),
    sa.Column('model', sa.String(length=120), nullable=True),
    sa.Column('crew', sa.Integer(), nullable=True),
    sa.Column('vehicle_class', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('vehicle_id')
    )
    op.create_table('favorites',
    sa.Column('date_added', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('favorite_characters', sa.Integer(), nullable=True),
    sa.Column('favorite_planets', sa.Integer(), nullable=True),
    sa.Column('favorite_vehicles', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['favorite_characters'], ['characters.name'], ),
    sa.ForeignKeyConstraint(['favorite_planets'], ['planets.name'], ),
    sa.ForeignKeyConstraint(['favorite_vehicles'], ['vehicles.name'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('date_added'),
    sa.UniqueConstraint('user_id')
    )
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('email', sa.VARCHAR(length=120), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('is_active', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('email', name='user_email_key')
    )
    op.drop_table('favorites')
    op.drop_table('vehicles')
    op.drop_table('users')
    op.drop_table('planets')
    op.drop_table('characters')
    # ### end Alembic commands ###