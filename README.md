# pymes-lms

Plataforma de capacitación para PYMES basada en competencias.

## Puesta en marcha

```bash
docker-compose up --build
```

El script de arranque espera a Postgres, aplica migraciones, ejecuta el seed e inicia backend y frontend.

- Backend: http://localhost:8000 (Swagger en `/docs`)
- Frontend: http://localhost:3000

## Credenciales demo
| Rol | Usuario | Contraseña |
|---|---|---|
| Empleado | empleado@example.com | demo |
| Líder | lider@example.com | demo |
| RRHH | rrhh@example.com | demo |
| Capacitador | capacitador@example.com | demo |
| Admin | admin@example.com | demo |

## Recorrido de prueba
1. Inicia sesión con un usuario demo.
2. Ingresa al dashboard y comienza el módulo de ejemplo.
3. Completa micro-lecciones, actividad y evaluación (0–100, recuperación si <80).
4. Revisa el feedback y competencias alcanzadas.
5. Ejecuta la DNC para detectar brechas y cursos sugeridos.
6. Consulta el ranking y los puntos acumulados.
7. Canjea una recompensa del catálogo.
8. Genera y descarga la constancia interna y el stub DC-3.

## Desarrollo
- Backend: FastAPI + PostgreSQL
- Frontend: Next.js + Tailwind

La configuración de variables está en `config/.env.example` y se copia automáticamente a `.env` y `frontend/.env.local` al iniciar.
