"""add_properties_in_data

Revision ID: 89c27d0e7e07
Revises: 5e39b15afd90
Create Date: 2017-09-07 00:34:44.354170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '89c27d0e7e07'
down_revision = '5e39b15afd90'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('controller_attribute_data', sa.Column('properties', sa.JSON(), nullable=True))
    op.add_column('controller_parameter_data', sa.Column('properties', sa.JSON(), nullable=True))
    op.add_column('controller_power_supply_attribute_data', sa.Column('properties', sa.JSON(), nullable=True))
    op.add_column('environment_sensor_attribute_data', sa.Column('properties', sa.JSON(), nullable=True))
    op.add_column('power_supply_attribute_data', sa.Column('properties', sa.JSON(), nullable=True))
    op.add_column('sensor_attribute_data', sa.Column('properties', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sensor_attribute_data', 'properties')
    op.drop_column('power_supply_attribute_data', 'properties')
    op.drop_column('environment_sensor_attribute_data', 'properties')
    op.drop_column('controller_power_supply_attribute_data', 'properties')
    op.drop_column('controller_parameter_data', 'properties')
    op.drop_column('controller_attribute_data', 'properties')
    # ### end Alembic commands ###