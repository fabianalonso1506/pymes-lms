# Arquitectura

La plataforma se compone de una arquitectura **frontend–backend** desacoplada con contenedores Docker orquestados mediante **docker-compose**.

## Backend
- **Framework:** FastAPI sobre Python.
- **Estructura:**
  - `app/main.py` expone la aplicación.
  - `app/api/` organiza routers por dominio.
  - `app/core/` maneja configuración, seguridad (OAuth2), hashing de contraseñas y utilidades.
  - `app/db/` integra SQLAlchemy y Alembic para modelos y migraciones.
  - `app/schemas/` define modelos Pydantic para validación de entrada/salida.
- **Endpoints principales:**
  - `POST /auth/signup` y `POST /auth/login` para registro y autenticación.
  - CRUD de `/users`, `/positions`, `/competencies`, `/courses`, `/modules`, `/assets`, `/rubrics`, `/assessments`, `/assessment-items`.
  - `/attempts` para guardar resultados y habilitar recuperación si el puntaje <80.
  - `/dnc` para procesar respuestas y proponer planes de capacitación.
  - `/learning-paths` para gestionar rutas de carrera.
  - `/rewards` y `/redemptions` para gamificación.
  - `/certificates` para generar constancias internas y DC-3 stub.
- **RBAC:** roles `empleado`, `líder`, `rrhh`, `capacitador`, `admin` controlados mediante dependencias de FastAPI.
- **Seguridad:**
  - Autenticación con OAuth2 y tokens JWT.
  - Contraseñas almacenadas con hashing bcrypt.
  - Validación y sanitización de entradas.
  - Logs estructurados y manejo de excepciones.
  - Preparado para HTTPS detrás de un proxy.

## Frontend
- **Framework:** Next.js con soporte SSR y modo SPA cuando aplica.
- **Estilos:** Tailwind CSS.
- **Estructura básica:**
  - `pages/` para rutas (login, dashboards, vista de módulo, recompensas).
  - `components/` reutilizables (navegación, tablas, cards, formularios).
  - `lib/` con cliente API.
  - `public/` para assets estáticos.
- **Integraciones clave:**
  - Consumo de API con autenticación JWT.
  - Flujos gamificados de módulos (1‑6).
  - Dashboards de empleado y RRHH con métricas y brechas.

## Base de Datos
- **Motor:** PostgreSQL.
- **Características:**
  - Tablas normalizadas para usuarios, posiciones, competencias, cursos, módulos y gamificación.
  - Uso de llaves foráneas para mantener integridad.
  - Migraciones gestionadas con Alembic.

## Preparación para Certificados y Recompensas
- Generación de constancias internas en PDF y plantilla **DC-3** stub.
- Hooks listos para integración con STPS y con proveedores externos.
- Catálogo de recompensas y flujo de canje con aprobaciones.

