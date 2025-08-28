from alembic import op
import sqlalchemy as sa

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    user_role = sa.Enum('empleado', 'lider', 'rrhh', 'capacitador', 'admin', name='user_role')
    competency_domain = sa.Enum('cognitive', 'psychomotor', 'affective', name='competency_domain')
    asset_type = sa.Enum('video', 'pdf', 'infographic', 'audio', name='asset_type')
    assessment_type = sa.Enum('diagnostic', 'formative', 'summative', name='assessment_type')
    redemption_status = sa.Enum('pending', 'approved', 'rejected', name='redemption_status')
    certificate_type = sa.Enum('internal', 'DC3_stub', name='certificate_type')

    user_role.create(op.get_bind(), checkfirst=True)
    competency_domain.create(op.get_bind(), checkfirst=True)
    asset_type.create(op.get_bind(), checkfirst=True)
    assessment_type.create(op.get_bind(), checkfirst=True)
    redemption_status.create(op.get_bind(), checkfirst=True)
    certificate_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('email', sa.Text(), nullable=False, unique=True),
        sa.Column('role', user_role, nullable=False, server_default='empleado'),
        sa.Column('hashed_password', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )

    op.create_table(
        'positions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('description', sa.Text())
    )

    op.create_table(
        'competencies',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('domain', competency_domain, nullable=False),
        sa.Column('level_required', sa.Integer())
    )

    op.create_table(
        'position_competencies',
        sa.Column('position_id', sa.Integer(), sa.ForeignKey('positions.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('competency_id', sa.Integer(), sa.ForeignKey('competencies.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('required_level', sa.Integer())
    )

    op.create_table(
        'courses',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('mandatory', sa.Boolean(), server_default=sa.text('false')),
        sa.Column('target_position_id', sa.Integer(), sa.ForeignKey('positions.id', ondelete='SET NULL'))
    )

    op.create_table(
        'modules',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id', ondelete='CASCADE')),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('order', sa.Integer(), nullable=False),
        sa.Column('weight_percent', sa.Integer())
    )
    op.create_index('ix_modules_course_order', 'modules', ['course_id', 'order'], unique=True)

    op.create_table(
        'assets',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id', ondelete='CASCADE')),
        sa.Column('type', asset_type, nullable=False),
        sa.Column('url', sa.Text(), nullable=False)
    )

    op.create_table(
        'rubrics',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id', ondelete='CASCADE')),
        sa.Column('criteria_json', sa.JSON()),
        sa.Column('weight_percent', sa.Integer())
    )

    op.create_table(
        'assessments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id', ondelete='CASCADE')),
        sa.Column('type', assessment_type, nullable=False),
        sa.Column('pass_score', sa.Integer())
    )

    op.create_table(
        'assessment_items',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('assessment_id', sa.Integer(), sa.ForeignKey('assessments.id', ondelete='CASCADE')),
        sa.Column('stem', sa.Text(), nullable=False),
        sa.Column('type', sa.Text(), nullable=False),
        sa.Column('options_json', sa.JSON()),
        sa.Column('answer_key', sa.Text())
    )

    op.create_table(
        'attempts',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('assessment_id', sa.Integer(), sa.ForeignKey('assessments.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('score', sa.Integer()),
        sa.Column('passed', sa.Boolean()),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )

    op.create_table(
        'evidences',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('module_id', sa.Integer(), sa.ForeignKey('modules.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('url', sa.Text()),
        sa.Column('notes', sa.Text())
    )

    op.create_table(
        'learning_paths',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('position_id', sa.Integer(), sa.ForeignKey('positions.id', ondelete='CASCADE')),
        sa.Column('name', sa.Text(), nullable=False)
    )

    op.create_table(
        'path_courses',
        sa.Column('path_id', sa.Integer(), sa.ForeignKey('learning_paths.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('order', sa.Integer())
    )

    op.create_table(
        'rewards',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.Text(), nullable=False),
        sa.Column('cost_points', sa.Integer()),
        sa.Column('description', sa.Text())
    )

    op.create_table(
        'user_points',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('points', sa.Integer(), server_default='0')
    )

    op.create_table(
        'redemptions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('reward_id', sa.Integer(), sa.ForeignKey('rewards.id', ondelete='CASCADE')),
        sa.Column('status', redemption_status, nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False)
    )
    op.create_index('ix_redemptions_user', 'redemptions', ['user_id'])

    op.create_table(
        'certificates',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE')),
        sa.Column('course_id', sa.Integer(), sa.ForeignKey('courses.id', ondelete='CASCADE')),
        sa.Column('type', certificate_type, nullable=False),
        sa.Column('issued_at', sa.DateTime()),
        sa.Column('folio', sa.Text())
    )

def downgrade():
    op.drop_table('certificates')
    op.drop_index('ix_redemptions_user', table_name='redemptions')
    op.drop_table('redemptions')
    op.drop_table('user_points')
    op.drop_table('rewards')
    op.drop_table('path_courses')
    op.drop_table('learning_paths')
    op.drop_table('evidences')
    op.drop_table('attempts')
    op.drop_table('assessment_items')
    op.drop_table('assessments')
    op.drop_table('rubrics')
    op.drop_table('assets')
    op.drop_index('ix_modules_course_order', table_name='modules')
    op.drop_table('modules')
    op.drop_table('courses')
    op.drop_table('position_competencies')
    op.drop_table('competencies')
    op.drop_table('positions')
    op.drop_table('users')

    certificate_type = sa.Enum('internal', 'DC3_stub', name='certificate_type')
    redemption_status = sa.Enum('pending', 'approved', 'rejected', name='redemption_status')
    assessment_type = sa.Enum('diagnostic', 'formative', 'summative', name='assessment_type')
    asset_type = sa.Enum('video', 'pdf', 'infographic', 'audio', name='asset_type')
    competency_domain = sa.Enum('cognitive', 'psychomotor', 'affective', name='competency_domain')
    user_role = sa.Enum('empleado', 'lider', 'rrhh', 'capacitador', 'admin', name='user_role')

    certificate_type.drop(op.get_bind(), checkfirst=True)
    redemption_status.drop(op.get_bind(), checkfirst=True)
    assessment_type.drop(op.get_bind(), checkfirst=True)
    asset_type.drop(op.get_bind(), checkfirst=True)
    competency_domain.drop(op.get_bind(), checkfirst=True)
    user_role.drop(op.get_bind(), checkfirst=True)
