"""Initial PostgreSQL schema and reserved exercise catalogue."""

from alembic import op
import sqlalchemy as sa

from app.db.seed import read_exercises


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    exercises = op.create_table('exercises',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False, start=100), nullable=False),
        sa.Column('name', sa.String(length=160), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('load_type', sa.String(length=20), server_default='external', nullable=False),
        sa.CheckConstraint("load_type IN ('external', 'bodyweight')", name=op.f('ck_exercises_load_type')),
        sa.CheckConstraint('length(btrim(name)) > 0', name=op.f('ck_exercises_name')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_exercises'))
    )
    op.bulk_insert(exercises, read_exercises())

    op.create_table('users',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('role', sa.String(length=20), server_default='user', nullable=False),
        sa.Column('is_blocked', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.CheckConstraint("email <> '' AND email = lower(btrim(email))", name=op.f('ck_users_normalized_email')),
        sa.CheckConstraint("role IN ('user', 'admin')", name=op.f('ck_users_role')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )
    op.create_table('auth_sessions',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('token_hash', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_auth_sessions_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_auth_sessions')),
        sa.UniqueConstraint('token_hash', name=op.f('uq_auth_sessions_token_hash'))
    )
    op.create_index('ix_auth_sessions_user_id_expires_at', 'auth_sessions', ['user_id', 'expires_at'], unique=False)
    op.create_table('body_weight_measurements',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('measured_on', sa.Date(), nullable=False),
        sa.Column('weight', sa.Numeric(precision=6, scale=2), nullable=False),
        sa.CheckConstraint('weight > 0', name=op.f('ck_body_weight_measurements_positive_weight')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_body_weight_measurements_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_body_weight_measurements')),
        sa.UniqueConstraint('user_id', 'measured_on', name=op.f('uq_body_weight_measurements_user_id_measured_on'))
    )
    op.create_table('friend_links',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('sender_id', sa.BigInteger(), nullable=False),
        sa.Column('recipient_id', sa.BigInteger(), nullable=False),
        sa.Column('status', sa.String(length=20), server_default='pending', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("status IN ('pending', 'accepted', 'rejected')", name=op.f('ck_friend_links_status')),
        sa.CheckConstraint('sender_id <> recipient_id', name=op.f('ck_friend_links_distinct_users')),
        sa.ForeignKeyConstraint(['recipient_id'], ['users.id'], name=op.f('fk_friend_links_recipient_id_users'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name=op.f('fk_friend_links_sender_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_friend_links'))
    )
    op.create_index('ix_friend_links_recipient_id_status', 'friend_links', ['recipient_id', 'status'], unique=False)
    op.create_index('uq_friend_pair', 'friend_links', [sa.literal_column('least(sender_id, recipient_id)'), sa.literal_column('greatest(sender_id, recipient_id)')], unique=True)
    op.create_table('notifications',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('kind', sa.String(length=40), nullable=False),
        sa.Column('subject_id', sa.String(length=80), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_notifications_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_notifications')),
        sa.UniqueConstraint('user_id', 'kind', 'subject_id', name=op.f('uq_notifications_user_id_kind_subject_id'))
    )
    op.create_table('profiles',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=120), server_default='', nullable=False),
        sa.Column('height', sa.Numeric(precision=5, scale=1), nullable=True),
        sa.Column('current_weight', sa.Numeric(precision=6, scale=2), nullable=True),
        sa.Column('goal', sa.String(length=200), nullable=True),
        sa.CheckConstraint('current_weight > 0', name=op.f('ck_profiles_positive_weight')),
        sa.CheckConstraint('height > 0', name=op.f('ck_profiles_positive_height')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_profiles_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_profiles')),
        sa.UniqueConstraint('user_id', name=op.f('uq_profiles_user_id'))
    )
    op.create_table('programs',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.CheckConstraint('length(btrim(name)) > 0', name=op.f('ck_programs_name')),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_programs_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_programs'))
    )
    op.create_index(op.f('ix_programs_user_id'), 'programs', ['user_id'], unique=False)
    op.create_table('training_groups',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('created_by', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint('length(btrim(name)) > 0', name=op.f('ck_training_groups_name')),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], name=op.f('fk_training_groups_created_by_users')),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_training_groups'))
    )
    op.create_table('user_achievements',
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('code', sa.String(length=40), nullable=False),
        sa.Column('awarded_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_achievements_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'code', name=op.f('pk_user_achievements'))
    )
    op.create_table('user_settings',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('show_weight_to_friends', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('show_stats_to_friends', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_user_settings_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_user_settings')),
        sa.UniqueConstraint('user_id', name=op.f('uq_user_settings_user_id'))
    )
    op.create_table('workouts',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_workouts_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_workouts'))
    )
    op.create_index('ix_workouts_user_id_date_id', 'workouts', ['user_id', 'date', 'id'], unique=False)
    op.create_table('group_members',
        sa.Column('group_id', sa.BigInteger(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['group_id'], ['training_groups.id'], name=op.f('fk_group_members_group_id_training_groups'), ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_group_members_user_id_users'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('group_id', 'user_id', name=op.f('pk_group_members'))
    )
    op.create_table('program_exercises',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('program_id', sa.BigInteger(), nullable=False),
        sa.Column('exercise_id', sa.BigInteger(), nullable=False),
        sa.Column('planned_sets', sa.Integer(), nullable=False),
        sa.Column('planned_reps', sa.Integer(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.CheckConstraint('planned_reps >= 0', name=op.f('ck_program_exercises_planned_reps')),
        sa.CheckConstraint('planned_sets > 0', name=op.f('ck_program_exercises_planned_sets')),
        sa.CheckConstraint('position > 0', name=op.f('ck_program_exercises_position')),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name=op.f('fk_program_exercises_exercise_id_exercises')),
        sa.ForeignKeyConstraint(['program_id'], ['programs.id'], name=op.f('fk_program_exercises_program_id_programs'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_program_exercises')),
        sa.UniqueConstraint('program_id', 'position', deferrable=True, initially='IMMEDIATE', name='uq_program_position')
    )
    op.create_table('workout_exercises',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('workout_id', sa.BigInteger(), nullable=False),
        sa.Column('exercise_id', sa.BigInteger(), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.CheckConstraint('position > 0', name=op.f('ck_workout_exercises_position')),
        sa.ForeignKeyConstraint(['exercise_id'], ['exercises.id'], name=op.f('fk_workout_exercises_exercise_id_exercises')),
        sa.ForeignKeyConstraint(['workout_id'], ['workouts.id'], name=op.f('fk_workout_exercises_workout_id_workouts'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_workout_exercises')),
        sa.UniqueConstraint('workout_id', 'position', name=op.f('uq_workout_exercises_workout_id_position'))
    )
    op.create_index('ix_workout_exercises_exercise_id_workout_id', 'workout_exercises', ['exercise_id', 'workout_id'], unique=False)
    op.create_table('workout_sets',
        sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
        sa.Column('workout_exercise_id', sa.BigInteger(), nullable=False),
        sa.Column('set_number', sa.Integer(), nullable=False),
        sa.Column('repetitions', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Numeric(precision=7, scale=2), nullable=False),
        sa.CheckConstraint('repetitions >= 0', name=op.f('ck_workout_sets_repetitions')),
        sa.CheckConstraint('set_number > 0', name=op.f('ck_workout_sets_set_number')),
        sa.CheckConstraint('weight >= 0', name=op.f('ck_workout_sets_weight')),
        sa.ForeignKeyConstraint(['workout_exercise_id'], ['workout_exercises.id'], name=op.f('fk_workout_sets_workout_exercise_id_workout_exercises'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_workout_sets')),
        sa.UniqueConstraint('workout_exercise_id', 'set_number', name=op.f('uq_workout_sets_workout_exercise_id_set_number'))
    )


def downgrade() -> None:
    op.drop_table('workout_sets')
    op.drop_index('ix_workout_exercises_exercise_id_workout_id', table_name='workout_exercises')
    op.drop_table('workout_exercises')
    op.drop_table('program_exercises')
    op.drop_table('group_members')
    op.drop_index('ix_workouts_user_id_date_id', table_name='workouts')
    op.drop_table('workouts')
    op.drop_table('user_settings')
    op.drop_table('user_achievements')
    op.drop_table('training_groups')
    op.drop_index(op.f('ix_programs_user_id'), table_name='programs')
    op.drop_table('programs')
    op.drop_table('profiles')
    op.drop_table('notifications')
    op.drop_index('uq_friend_pair', table_name='friend_links')
    op.drop_index('ix_friend_links_recipient_id_status', table_name='friend_links')
    op.drop_table('friend_links')
    op.drop_table('body_weight_measurements')
    op.drop_index('ix_auth_sessions_user_id_expires_at', table_name='auth_sessions')
    op.drop_table('auth_sessions')
    op.drop_table('users')
    op.drop_table('exercises')
