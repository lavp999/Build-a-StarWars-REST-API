"""empty message

Revision ID: a27a03aeb96d
Revises: a894445afa20
Create Date: 2022-12-02 22:12:25.297514

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a27a03aeb96d'
down_revision = 'a894445afa20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.drop_constraint('character_id_planet_fkey', type_='foreignkey')
        batch_op.drop_column('id_planet')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('character', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_planet', sa.INTEGER(), autoincrement=False, nullable=True))
        batch_op.create_foreign_key('character_id_planet_fkey', 'planet', ['id_planet'], ['id'])

    # ### end Alembic commands ###
