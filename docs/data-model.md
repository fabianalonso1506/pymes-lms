# Modelo de Datos

A continuación se describen las tablas y relaciones principales del LMS.

## users
- `id` (PK, serial)
- `name` (text, no nulo)
- `email` (text, único, no nulo)
- `role` (enum: empleado|líder|rrhh|capacitador|admin)
- `hashed_password` (text, no nulo)
- `created_at` (timestamp, default now)

## positions
- `id` (PK, serial)
- `name` (text, no nulo)
- `description` (text)

## competencies
- `id` (PK, serial)
- `name` (text, no nulo)
- `domain` (enum: cognitive|psychomotor|affective)
- `level_required` (int)

## position_competencies
- `position_id` (FK → positions.id)
- `competency_id` (FK → competencies.id)
- `required_level` (int)
- **PK compuesta:** (position_id, competency_id)

## courses
- `id` (PK, serial)
- `title` (text, no nulo)
- `description` (text)
- `mandatory` (boolean, default false)
- `target_position_id` (FK → positions.id)

## modules
- `id` (PK, serial)
- `course_id` (FK → courses.id)
- `title` (text, no nulo)
- `order` (int, no nulo)
- `weight_percent` (int, 0-100)

## assets
- `id` (PK, serial)
- `module_id` (FK → modules.id)
- `type` (enum: video|pdf|infographic|audio)
- `url` (text, no nulo)

## rubrics
- `id` (PK, serial)
- `module_id` (FK → modules.id)
- `criteria_json` (jsonb)
- `weight_percent` (int, 0-100)

## assessments
- `id` (PK, serial)
- `module_id` (FK → modules.id)
- `type` (enum: diagnostic|formative|summative)
- `pass_score` (int, 0-100)

## assessment_items
- `id` (PK, serial)
- `assessment_id` (FK → assessments.id)
- `stem` (text, no nulo)
- `type` (text: opción múltiple, abierto, etc.)
- `options_json` (jsonb)
- `answer_key` (text)

## attempts
- `id` (PK, serial)
- `assessment_id` (FK → assessments.id)
- `user_id` (FK → users.id)
- `score` (int, 0-100)
- `passed` (boolean)
- `created_at` (timestamp, default now)

## evidences
- `id` (PK, serial)
- `module_id` (FK → modules.id)
- `user_id` (FK → users.id)
- `url` (text)
- `notes` (text)

## learning_paths
- `id` (PK, serial)
- `position_id` (FK → positions.id)
- `name` (text, no nulo)

## path_courses
- `path_id` (FK → learning_paths.id)
- `course_id` (FK → courses.id)
- `order` (int)
- **PK compuesta:** (path_id, course_id)

## rewards
- `id` (PK, serial)
- `name` (text, no nulo)
- `cost_points` (int)
- `description` (text)

## user_points
- `user_id` (PK, FK → users.id)
- `points` (int, default 0)

## redemptions
- `id` (PK, serial)
- `user_id` (FK → users.id)
- `reward_id` (FK → rewards.id)
- `status` (enum: pending|approved|rejected)
- `created_at` (timestamp, default now)

## certificates
- `id` (PK, serial)
- `user_id` (FK → users.id)
- `course_id` (FK → courses.id)
- `type` (enum: internal|DC3_stub)
- `issued_at` (timestamp)
- `folio` (text)

