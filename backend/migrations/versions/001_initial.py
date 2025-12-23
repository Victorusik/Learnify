"""initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2025-01-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('level', sa.Integer(), nullable=True),
        sa.Column('xp', sa.Integer(), nullable=True),
        sa.Column('streak', sa.Integer(), nullable=True),
        sa.Column('daily_goal', sa.Integer(), nullable=True),
        sa.Column('completed_today', sa.Integer(), nullable=True),
        sa.Column('selected_categories', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('notifications', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories_id'), 'categories', ['id'], unique=False)

    # Create courses table
    op.create_table(
        'courses',
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('category_id', sa.String(), nullable=False),
        sa.Column('subcategory', sa.String(), nullable=False),
        sa.Column('level', sa.String(), nullable=False),
        sa.Column('difficulty_score', sa.Integer(), nullable=False),
        sa.Column('estimated_duration_weeks', sa.Integer(), nullable=False),
        sa.Column('estimated_duration_hours', sa.Integer(), nullable=False),
        sa.Column('total_lessons', sa.Integer(), nullable=False),
        sa.Column('total_practice_tasks', sa.Integer(), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('author', sa.String(), nullable=False),
        sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_updated', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('language', sa.String(), nullable=True),
        sa.Column('target_audience', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('completion_certificate', sa.Boolean(), nullable=True),
        sa.Column('short_description', sa.String(), nullable=False),
        sa.Column('full_description', sa.String(), nullable=False),
        sa.Column('learning_outcomes', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('prerequisites', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('cover_image_url', sa.String(), nullable=False),
        sa.Column('promo_video_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
        sa.PrimaryKeyConstraint('course_id')
    )
    op.create_index(op.f('ix_courses_course_id'), 'courses', ['course_id'], unique=False)

    # Create lessons table
    op.create_table(
        'lessons',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lessons_id'), 'lessons', ['id'], unique=False)

    # Create blocks table
    op.create_table(
        'blocks',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('lesson_id', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('subtype', sa.String(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('question', sa.String(), nullable=True),
        sa.Column('options', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('hints', postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column('correct_answer', sa.String(), nullable=True),
        sa.Column('explanation', sa.String(), nullable=True),
        sa.Column('sample_answer', sa.String(), nullable=True),
        sa.Column('answer', sa.String(), nullable=True),
        sa.Column('visualization_hint', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_blocks_id'), 'blocks', ['id'], unique=False)

    # Create achievements table
    op.create_table(
        'achievements',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), nullable=False),
        sa.Column('max_progress', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_achievements_id'), 'achievements', ['id'], unique=False)

    # Create user_courses table
    op.create_table(
        'user_courses',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('enrolled_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_courses_id'), 'user_courses', ['id'], unique=False)

    # Create user_progress table
    op.create_table(
        'user_progress',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('block_id', sa.String(), nullable=False),
        sa.Column('lesson_id', sa.String(), nullable=False),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_progress_id'), 'user_progress', ['id'], unique=False)

    # Create repetition_data table
    op.create_table(
        'repetition_data',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('block_id', sa.String(), nullable=False),
        sa.Column('lesson_id', sa.String(), nullable=False),
        sa.Column('course_id', sa.String(), nullable=False),
        sa.Column('last_review', sa.DateTime(timezone=True), nullable=True),
        sa.Column('next_review', sa.DateTime(timezone=True), nullable=True),
        sa.Column('interval', sa.Integer(), nullable=True),
        sa.Column('ease_factor', sa.Float(), nullable=True),
        sa.Column('needs_review', sa.Boolean(), nullable=True),
        sa.Column('mistakes', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['block_id'], ['blocks.id'], ),
        sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
        sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_repetition_data_id'), 'repetition_data', ['id'], unique=False)

    # Create user_achievements table
    op.create_table(
        'user_achievements',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('achievement_id', sa.String(), nullable=False),
        sa.Column('unlocked_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('progress', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['achievement_id'], ['achievements.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_achievements_id'), 'user_achievements', ['id'], unique=False)

    # Create user_statistics table
    op.create_table(
        'user_statistics',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('total_lessons', sa.Integer(), nullable=True),
        sa.Column('average_accuracy', sa.Float(), nullable=True),
        sa.Column('days_learning', sa.Integer(), nullable=True),
        sa.Column('total_cards_reviewed', sa.Integer(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_user_statistics_id'), 'user_statistics', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_statistics_id'), table_name='user_statistics')
    op.drop_table('user_statistics')
    op.drop_index(op.f('ix_user_achievements_id'), table_name='user_achievements')
    op.drop_table('user_achievements')
    op.drop_index(op.f('ix_repetition_data_id'), table_name='repetition_data')
    op.drop_table('repetition_data')
    op.drop_index(op.f('ix_user_progress_id'), table_name='user_progress')
    op.drop_table('user_progress')
    op.drop_index(op.f('ix_user_courses_id'), table_name='user_courses')
    op.drop_table('user_courses')
    op.drop_index(op.f('ix_achievements_id'), table_name='achievements')
    op.drop_table('achievements')
    op.drop_index(op.f('ix_blocks_id'), table_name='blocks')
    op.drop_table('blocks')
    op.drop_index(op.f('ix_lessons_id'), table_name='lessons')
    op.drop_table('lessons')
    op.drop_index(op.f('ix_courses_course_id'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_categories_id'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')

