import os
import json
import sys
from sqlalchemy import create_engine, text

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from backend.app.core.security import get_password_hash

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/lms')

def main():
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        # positions
        conn.execute(
            text('INSERT INTO positions (name, description) VALUES (:name, :desc)'),
            [
                {'name': 'Ventas', 'desc': 'Área de ventas'},
                {'name': 'Técnico', 'desc': 'Área técnica'},
            ],
        )
        positions = conn.execute(text('SELECT id, name FROM positions')).fetchall()
        pos_ids = {row.name: row.id for row in positions}

        # learning paths
        conn.execute(
            text('INSERT INTO learning_paths (position_id, name) VALUES (:position_id, :name)'),
            [
                {'position_id': pos_ids['Ventas'], 'name': 'Ruta Ventas'},
                {'position_id': pos_ids['Técnico'], 'name': 'Ruta Técnico'},
            ],
        )
        paths = conn.execute(text('SELECT id, position_id FROM learning_paths')).fetchall()
        path_ids = {row.position_id: row.id for row in paths}

        # demo users
        password = get_password_hash('demo')
        demo_users = [
            {'name': 'Empleado Demo', 'email': 'empleado@example.com', 'role': 'empleado'},
            {'name': 'Líder Demo', 'email': 'lider@example.com', 'role': 'lider'},
            {'name': 'RRHH Demo', 'email': 'rrhh@example.com', 'role': 'rrhh'},
            {'name': 'Capacitador Demo', 'email': 'capacitador@example.com', 'role': 'capacitador'},
            {'name': 'Admin Demo', 'email': 'admin@example.com', 'role': 'admin'},
        ]
        for u in demo_users:
            res = conn.execute(
                text('INSERT INTO users (name, email, role, hashed_password) VALUES (:name, :email, :role, :pwd) RETURNING id'),
                {**u, 'pwd': password},
            )
            user_id = res.fetchone()[0]
            conn.execute(text('INSERT INTO user_points (user_id, points) VALUES (:uid, 0)'), {'uid': user_id})

        # courses
        conn.execute(
            text('INSERT INTO courses (title, description, mandatory, target_position_id) VALUES (:title, :desc, :mand, :pos_id)'),
            [
                {'title': 'Introducción a Ventas', 'desc': 'Curso base para ventas', 'mand': True, 'pos_id': pos_ids['Ventas']},
                {'title': 'Fundamentos Técnicos', 'desc': 'Curso base para técnicos', 'mand': True, 'pos_id': pos_ids['Técnico']},
            ],
        )
        courses = conn.execute(text('SELECT id, target_position_id FROM courses')).fetchall()
        course_ids = {row.target_position_id: row.id for row in courses}

        # link path_courses
        conn.execute(
            text('INSERT INTO path_courses (path_id, course_id, "order") VALUES (:path_id, :course_id, :order)'),
            [
                {'path_id': path_ids[pos_ids['Ventas']], 'course_id': course_ids[pos_ids['Ventas']], 'order': 1},
                {'path_id': path_ids[pos_ids['Técnico']], 'course_id': course_ids[pos_ids['Técnico']], 'order': 1},
            ],
        )

        # modules
        conn.execute(
            text('INSERT INTO modules (course_id, title, "order", weight_percent) VALUES (:course_id, :title, :order, :weight)'),
            [
                {'course_id': course_ids[pos_ids['Ventas']], 'title': 'Módulo Ventas 1', 'order': 1, 'weight': 100},
                {'course_id': course_ids[pos_ids['Técnico']], 'title': 'Módulo Técnico 1', 'order': 1, 'weight': 100},
            ],
        )
        modules = conn.execute(text('SELECT id, course_id FROM modules')).fetchall()
        module_ids = {row.course_id: row.id for row in modules}

        # assets
        conn.execute(
            text('INSERT INTO assets (module_id, type, url) VALUES (:module_id, :type, :url)'),
            [
                {'module_id': module_ids[course_ids[pos_ids['Ventas']]], 'type': 'video', 'url': 'https://example.com/ventas/video.mp4'},
                {'module_id': module_ids[course_ids[pos_ids['Ventas']]], 'type': 'infographic', 'url': 'https://example.com/ventas/infografia.png'},
                {'module_id': module_ids[course_ids[pos_ids['Técnico']]], 'type': 'video', 'url': 'https://example.com/tecnico/video.mp4'},
                {'module_id': module_ids[course_ids[pos_ids['Técnico']]], 'type': 'infographic', 'url': 'https://example.com/tecnico/infografia.png'},
            ],
        )

        # rubrics
        rubric = json.dumps({'criterios': [{'descripcion': 'Compleción', 'valor': 100}]})
        conn.execute(
            text('INSERT INTO rubrics (module_id, criteria_json, weight_percent) VALUES (:module_id, :criteria, :weight)'),
            [
                {'module_id': module_ids[course_ids[pos_ids['Ventas']]], 'criteria': rubric, 'weight': 100},
                {'module_id': module_ids[course_ids[pos_ids['Técnico']]], 'criteria': rubric, 'weight': 100},
            ],
        )

        # assessments
        conn.execute(
            text('INSERT INTO assessments (module_id, type, pass_score) VALUES (:module_id, :type, :pass)'),
            [
                {'module_id': module_ids[course_ids[pos_ids['Ventas']]], 'type': 'summative', 'pass': 80},
                {'module_id': module_ids[course_ids[pos_ids['Técnico']]], 'type': 'summative', 'pass': 80},
            ],
        )
        assessments = conn.execute(text('SELECT id, module_id FROM assessments')).fetchall()
        assessment_ids = {row.module_id: row.id for row in assessments}

        # assessment items helper
        def mcq(stem, answer):
            return {
                'stem': stem,
                'type': 'multiple_choice',
                'options': json.dumps(['A', 'B', 'C', 'D']),
                'answer': answer,
            }

        def tfq(stem, answer):
            return {
                'stem': stem,
                'type': 'true_false',
                'options': json.dumps(['True', 'False']),
                'answer': answer,
            }

        items_sales = [
            mcq('Ventas P1', 'A'),
            mcq('Ventas P2', 'B'),
            mcq('Ventas P3', 'C'),
            tfq('Ventas P4', 'True'),
            tfq('Ventas P5', 'False'),
        ]
        items_tech = [
            mcq('Técnico P1', 'A'),
            mcq('Técnico P2', 'B'),
            mcq('Técnico P3', 'C'),
            tfq('Técnico P4', 'True'),
            tfq('Técnico P5', 'False'),
        ]

        for course_id, items in [
            (course_ids[pos_ids['Ventas']], items_sales),
            (course_ids[pos_ids['Técnico']], items_tech),
        ]:
            assessment_id = assessment_ids[module_ids[course_id]]
            for item in items:
                conn.execute(
                    text('INSERT INTO assessment_items (assessment_id, stem, type, options_json, answer_key) VALUES (:aid, :stem, :type, :opts, :ans)'),
                    {
                        'aid': assessment_id,
                        'stem': item['stem'],
                        'type': item['type'],
                        'opts': item['options'],
                        'ans': item['answer'],
                    },
                )

        # rewards
        conn.execute(
            text('INSERT INTO rewards (name, cost_points, description) VALUES (:name, :cost, :desc)'),
            [
                {'name': 'Vale comida', 'cost': 100, 'desc': 'Vale para comida'},
                {'name': '1h extra de comida', 'cost': 200, 'desc': 'Tiempo adicional de comida'},
            ],
        )

    print('Seed data inserted')


if __name__ == '__main__':
    main()
