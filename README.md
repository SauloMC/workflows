# CI/CD + Feature Flags Demo

Este repositorio es una base mínima de ejemplo para un pipeline de CI/CD con validaciones automáticas, despliegue a staging, aprobación manual para producción y feature flags seguros.

## Stack detectado

Como el repositorio estaba vacío, se preparó una implementación mínima con:

- Python 3.12 para la API/backend de ejemplo.
- React + Vite para una interfaz de frontend mínima.
- GitHub Actions para CI/CD.
- Despliegue desacoplado mediante un script `scripts/deploy.sh`, listo para conectarse con un proveedor externo (por ejemplo, SSH a un VPS, un host de nube o un servicio de hosting con webhook).

## Flujo de despliegue

### 1) Pull Request

Cada PR ejecuta el workflow de CI, que:

- instala dependencias,
- compila el frontend,
- ejecuta lint,
- ejecuta tests,
- falla si alguna validación falla,
- no despliega a producción.

### 2) Merge o push a main

Cuando se fusiona a `main`, el workflow de staging:

- vuelve a validar QA de código,
- hace build,
- despliega automáticamente a `staging`,
- publica un resumen en el check del workflow.

### 3) Producción

La producción se activa mediante `workflow_dispatch` en GitHub Actions y requiere:

- entorno `production` configurado en GitHub,
- aprobación manual del reviewer,
- rama `main` como origen,
- secret `DEPLOY_HOST` y `DEPLOY_USER` (y opcionalmente `DEPLOY_PORT`/`DEPLOY_PATH`),
- variables del entorno `DEPLOY_PORT`, `DEPLOY_PATH`, `STAGING_URL`, `PRODUCTION_URL` si se usan.

Para evitar despliegues simultáneos se usa `concurrency`.

## Feature flags

Se implementó un feature flag centralizado para Python y un flag de entorno compatible con React/Vite.

### Flag de ejemplo

- `NEW_DASHBOARD_ENABLED`
- Valor por defecto: `false`
- En backend: variable de entorno `NEW_DASHBOARD_ENABLED`
- En frontend: variable de build `VITE_NEW_DASHBOARD_ENABLED`

### Backend

Se puede leer con:

```python
from feature_flags import get_flag

if get_flag("NEW_DASHBOARD_ENABLED"):
    render_new_dashboard()
```

### Frontend

Se usa en Vite con:

```jsx
const isNewDashboardEnabled = import.meta.env.VITE_NEW_DASHBOARD_ENABLED === 'true'
```

## Cómo activar, desactivar y revertir

### Activar en staging

Agregar en GitHub → Settings → Environments → `staging`:

- `NEW_DASHBOARD_ENABLED=true` en variables del entorno o exportarlo en la shell del runner.

### Activar en producción

En GitHub → Settings → Environments → `production`:

- `NEW_DASHBOARD_ENABLED=true`
- Luego aprobar el deployment manualmente.

### Desactivar rápidamente

Cambiar el valor a `false` en el entorno correspondiente o borrar la variable. Eso hace rollback operativo sin cambiar código.

### Rollout gradual

- Empieza apagado por defecto.
- Actívalo solo en `staging`.
- Verifica métricas y flujo.
- Luego habilítalo en producción con aprobación.
- Si ocurre un problema, vuelve a `false` y rehaz el despliegue.

## Secrets y configuración en GitHub

Configura esto en GitHub según tu proveedor:

- Secrets:
  - `DEPLOY_HOST`
  - `DEPLOY_USER`
  - `DEPLOY_SSH_PRIVATE_KEY` (si usas SSH key en un script más avanzado)
- Variables:
  - `DEPLOY_PORT` (opcional)
  - `DEPLOY_PATH` (opcional)
  - `STAGING_URL`
  - `PRODUCTION_URL`
  - `NEW_DASHBOARD_ENABLED` en el entorno correspondiente

Nunca agregues secretos al repositorio, ni en YAML, ni en logs, ni en archivos versionados.

## Cómo agregar un nuevo feature flag

1. Define el nombre en el backend en `backend/feature_flags.py`.
2. Añade la variable a `.env.example`.
3. Si aplica a frontend, usa la variable `VITE_<NOMBRE>`.
4. Añade una prueba unitária para validar el comportamiento por defecto y activado.
5. Usa el flag con un guard de seguridad en la lógica de negocio o UI.

## Ejecutar localmente

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
export NEW_DASHBOARD_ENABLED=false
python app.py
```

### Frontend

```bash
cd frontend
npm install
export VITE_NEW_DASHBOARD_ENABLED=false
npm run dev
```

### Tests

```bash
cd backend
pytest -q

cd ../frontend
npm test
npm run build
```

## Proveedor de despliegue detectado

No había un proveedor de hosting configurado en el repositorio. Por eso dejé el pipeline preparado con un script `deploy.sh` desacoplado y la fila de configuración declarativa para SSH/hosting externo.

Faltan credenciales o configuración concretas del proveedor real, por ejemplo:

- `DEPLOY_HOST` (servidor o host remoto)
- `DEPLOY_USER` (usuario SSH o usuario del hosting)
- `DEPLOY_PATH` (ruta remota de despliegue)
- `DEPLOY_PORT` (opcional)
- Si usas un proveedor específico, además necesitarás las credenciales del servicio correspondiente (por ejemplo, Azure App Service, VPS, Railway, Render, Vercel, Netlify, etc.).

## Archivos principales

- `.github/workflows/ci.yml`
- `.github/workflows/staging.yml`
- `.github/workflows/production.yml`
- `backend/feature_flags.py`
- `backend/app.py`
- `backend/test_feature_flags.py`
- `frontend/src/App.jsx`
- `frontend/src/App.test.jsx`
- `scripts/deploy.sh`
- `.env.example`
