"""empty message

Revision ID: 87ff07e361e5
Revises: 
Create Date: 2021-06-24 22:38:45.090117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87ff07e361e5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('realstate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('location', sa.String(length=500), nullable=True),
    sa.Column('total_area', sa.Integer(), nullable=True),
    sa.Column('builded_surface', sa.Integer(), nullable=True),
    sa.Column('rooms', sa.Integer(), nullable=True),
    sa.Column('bathrooms', sa.Integer(), nullable=True),
    sa.Column('parkings', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('id_realState', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_realState'], ['realstate.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('real_state_agency')
    op.drop_table('real_state')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('real_state',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(length=150), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('location', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
    sa.Column('total_area', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('builded_surface', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('rooms', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bathrooms', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('parkings', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='real_state_pkey')
    )
    op.create_table('real_state_agency',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('company', sa.VARCHAR(length=30), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(length=900), autoincrement=False, nullable=False),
    sa.Column('location', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('team_agents', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('listings', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_verified', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='real_state_agency_pkey'),
    sa.UniqueConstraint('company', name='real_state_agency_company_key'),
    sa.UniqueConstraint('description', name='real_state_agency_description_key'),
    sa.UniqueConstraint('listings', name='real_state_agency_listings_key'),
    sa.UniqueConstraint('location', name='real_state_agency_location_key')
    )
    op.drop_table('transaction')
    op.drop_table('realstate')
    # ### end Alembic commands ###
