"""user table

Revision ID: 81f382be67e9
Revises: 
Create Date: 2021-04-27 13:57:14.236132

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81f382be67e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('condition',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.PickleType(), nullable=True),
    sa.Column('nonverbal', sa.PickleType(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('condition_id', sa.Integer(), nullable=True),
    sa.Column('code', sa.String(length=20), nullable=True),
    sa.Column('feedback_counts', sa.PickleType(), nullable=True),
    sa.Column('consent', sa.Integer(), nullable=True),
    sa.Column('training', sa.Integer(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('ethnicity', sa.Integer(), nullable=True),
    sa.Column('education', sa.Integer(), nullable=True),
    sa.Column('robot', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['condition_id'], ['condition.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('demo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('round_num', sa.Integer(), nullable=True),
    sa.Column('demo_num', sa.Integer(), nullable=True),
    sa.Column('card_num', sa.Integer(), nullable=True),
    sa.Column('correct_bin', sa.PickleType(), nullable=True),
    sa.Column('rule_set', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demo_timestamp'), 'demo', ['timestamp'], unique=False)
    op.create_table('survey',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('round_num', sa.Integer(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=True),
    sa.Column('user_learning', sa.Integer(), nullable=True),
    sa.Column('animacy1', sa.Integer(), nullable=True),
    sa.Column('animacy2', sa.Integer(), nullable=True),
    sa.Column('animacy3', sa.Integer(), nullable=True),
    sa.Column('intelligence1', sa.Integer(), nullable=True),
    sa.Column('intelligence2', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_survey_timestamp'), 'survey', ['timestamp'], unique=False)
    op.create_table('trial',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('round_num', sa.Integer(), nullable=True),
    sa.Column('trial_num', sa.Integer(), nullable=True),
    sa.Column('card_num', sa.Integer(), nullable=True),
    sa.Column('correct_bin', sa.PickleType(), nullable=True),
    sa.Column('chosen_bin', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.Integer(), nullable=True),
    sa.Column('rule_set', sa.PickleType(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trial_timestamp'), 'trial', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_trial_timestamp'), table_name='trial')
    op.drop_table('trial')
    op.drop_index(op.f('ix_survey_timestamp'), table_name='survey')
    op.drop_table('survey')
    op.drop_index(op.f('ix_demo_timestamp'), table_name='demo')
    op.drop_table('demo')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('condition')
    # ### end Alembic commands ###
