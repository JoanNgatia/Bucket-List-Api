"""empty message

Revision ID: 4f563d5813fe
Revises: None
Create Date: 2016-02-22 11:19:24.204766

"""

# revision identifiers, used by Alembic.
revision = '4f563d5813fe'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bucketlist')
    op.drop_table('user')
    op.drop_table('bucketlistitems')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bucketlistitems',
    sa.Column('item_id', sa.INTEGER(), nullable=False),
    sa.Column('item_name', sa.VARCHAR(), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('date_modified', sa.DATETIME(), nullable=True),
    sa.Column('done', sa.BOOLEAN(), nullable=True),
    sa.Column('bucket_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['bucket_id'], [u'bucketlist.list_id'], ),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(), nullable=False),
    sa.Column('password_hash', sa.VARCHAR(), nullable=True),
    sa.Column('confirmed', sa.BOOLEAN(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('bucketlist',
    sa.Column('list_id', sa.INTEGER(), nullable=False),
    sa.Column('list_name', sa.VARCHAR(), nullable=False),
    sa.Column('creator', sa.INTEGER(), nullable=True),
    sa.Column('date_created', sa.DATETIME(), nullable=True),
    sa.Column('date_modified', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['creator'], [u'user.user_id'], ),
    sa.PrimaryKeyConstraint('list_id')
    )
    ### end Alembic commands ###