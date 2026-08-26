# Guion de presentación: CI/CD + Feature Flags

Guía paso a paso para demostrar el pipeline en vivo, con un cambio real en el proyecto.

---

## Conceptos básicos (explicar antes de tocar código, 5-8 min)

Esta sección es para explicar a alguien que no sabe nada de estos términos. Úsala como guion, en orden, antes de tocar el editor.

### ¿Qué es un pipeline?

**Qué decir:**
> "Un pipeline es simplemente una serie de pasos automáticos que se ejecutan en orden cada vez que pasa algo, por ejemplo cada vez que alguien sube código. Es como una línea de producción de una fábrica: el código entra por un lado, pasa por varias estaciones de control (revisar, probar, armar), y sale listo para usarse."

**Analogía simple:**
> "Imaginen que quieren enviar una carta importante. Antes de enviarla, alguien la revisa, corrige errores, la mete en un sobre y la sella. Eso es un pipeline: pasos automáticos, siempre en el mismo orden, para que nada llegue a su destino sin pasar por control de calidad."

### ¿Qué es CI/CD?

**Qué decir:**
> "CI/CD son dos siglas que casi siempre van juntas: Integración Continua y Entrega/Despliegue Continuo."

- **CI (Integración Continua):** cada vez que alguien propone un cambio de código, el sistema automáticamente lo revisa: ¿compila?, ¿pasa las pruebas?, ¿tiene errores de estilo? Si algo falla, se detiene ahí, antes de que el cambio llegue a afectar a nadie más.
- **CD (Entrega/Despliegue Continuo):** una vez que el código pasó todas las revisiones, el sistema lo lleva automáticamente (o con un solo clic) a un ambiente donde la gente lo puede usar, como un sitio web en internet.

**Analogía simple:**
> "CI es como el control de calidad antes de que un producto salga de la fábrica. CD es la parte de logística que lleva el producto ya aprobado hasta la tienda."

### ¿Qué es un Pull Request (PR)?

**Qué decir:**
> "Un Pull Request es una propuesta de cambio. Cuando alguien quiere modificar el código, no lo mete directo al proyecto principal; primero abre un PR, que es como decir 'oye, quiero agregar esto, revísenlo antes de aceptarlo'. Ahí es donde se dispara automáticamente el pipeline de CI para revisar ese cambio."

### ¿Qué son los ambientes (staging y producción)?

**Qué decir:**
> "No todos los cambios van directo a donde los usuarios reales los ven. Normalmente hay ambientes intermedios."

- **Staging:** una copia casi idéntica del ambiente real, pero privada, donde se prueba que todo funcione antes de mostrarlo al público.
- **Producción:** el ambiente real, el que usan los usuarios finales. Aquí los errores sí importan y cuestan caro, por eso se protege más.

**Analogía simple:**
> "Staging es como el ensayo general antes de una obra de teatro. Producción es la noche del estreno, con público real."

### ¿Qué es una aprobación manual?

**Qué decir:**
> "Aunque todo esté automatizado, para producción dejamos un punto donde una persona tiene que decir 'sí, adelante'. Es un freno de seguridad: la máquina hace todo el trabajo pesado, pero la decisión final la toma un humano."

### ¿Qué es un feature flag?

**Qué decir:**
> "Un feature flag, o 'bandera de funcionalidad', es un interruptor que prende o apaga una parte del código sin necesidad de subir un cambio nuevo. Se controla con una variable de configuración, no con código."

**Analogía simple:**
> "Es como el interruptor de la luz de un cuarto que ya está cableado. La instalación eléctrica (el código) ya está lista y desplegada, pero la luz (la funcionalidad) solo se enciende cuando alguien mueve el interruptor (activa la variable). Si algo sale mal, apagas la luz al instante, sin tener que romper la pared para desconectar el cable."

**Por qué es útil:**
> "Permite subir código a producción ya integrado, pero apagado, y encenderlo cuando estemos seguros. Y si algo falla después de encenderlo, lo apagamos en segundos, sin tener que deshacer el código ni hacer un nuevo despliegue."

### ¿Qué son los secretos (secrets) y variables de entorno?

**Qué decir:**
> "Un secreto es información sensible, como una contraseña o una llave de acceso, que nunca debe escribirse directamente en el código porque cualquiera que vea el repositorio la vería. En su lugar, se guarda en un lugar seguro (en este caso, la configuración de GitHub) y el pipeline la usa en el momento sin mostrarla."

> "Una variable de entorno es simplemente un valor de configuración que vive fuera del código y que el programa lee cuando se ejecuta. Los feature flags, por ejemplo, se controlan con variables de entorno."

### ¿Qué es `concurrency` (evitar despliegues simultáneos)?

**Qué decir:**
> "Si dos despliegues al mismo ambiente ocurren al mismo tiempo, se pueden pisar entre sí y dejar el sistema en un estado inconsistente. Por eso configuramos una regla que dice: 'si ya hay un despliegue en curso a este ambiente, espera o cancela el anterior, pero nunca los dejes correr los dos a la vez'."

### Resumen de todo, en una sola frase por concepto

| Concepto | En una frase |
|---|---|
| Pipeline | Pasos automáticos que se ejecutan en orden. |
| CI | Revisar el código automáticamente antes de aceptarlo. |
| CD | Llevar el código ya aprobado hasta donde se usa. |
| Pull Request | Propuesta de cambio que se revisa antes de aceptarse. |
| Staging | Ambiente de prueba, no lo ve el público. |
| Producción | Ambiente real, lo usan los usuarios de verdad. |
| Aprobación manual | Un humano da el visto bueno final. |
| Feature flag | Interruptor para prender/apagar una función sin redeploy. |
| Secreto | Dato sensible que nunca va en el código. |
| Concurrency | Regla para no desplegar dos veces a la vez al mismo lugar. |

### Qué estamos haciendo en este proyecto, en palabras simples

**Qué decir:**
> "En este proyecto armamos todo ese proceso de punta a punta: cuando alguien propone un cambio, se revisa solo; cuando se aprueba y se une al proyecto principal, se prueba en un ambiente seguro llamado staging; y para que llegue al público (producción), se necesita que una persona lo apruebe manualmente. Además, agregamos una funcionalidad nueva que viene apagada por defecto, y la podemos encender o apagar con un interruptor (feature flag), sin tener que tocar código ni volver a desplegar."

---

## 0) Antes de empezar (preparación, 2 min)

Abre 3 cosas en pantalla:
1. El editor con este repo.
2. La pestaña **Actions** del repositorio en GitHub.
3. La pestaña **Settings → Environments** del repositorio.

Ten listo el comando de verificación local:

```powershell
Set-Location 'C:\Users\IanSa\workflows\backend'; & '../.venv/Scripts/python.exe' -m pytest -q; Set-Location '../frontend'; npm test -- --run; npm run build
```

---

## 1) Explicar la arquitectura (2 min)

**Qué decir:**
> "Este proyecto tiene un backend en Python (Flask) y un frontend en React con Vite. No es la app en sí lo importante, sino el pipeline: cómo el código pasa de un Pull Request a staging, y de staging a producción con aprobación manual."

**Qué mostrar:** estructura de carpetas:
- [backend/](backend) → API + feature flags
- [frontend/](frontend) → UI + feature flags
- [.github/workflows/](.github/workflows) → CI, staging, producción
- [scripts/deploy.sh](scripts/deploy.sh) → despliegue desacoplado

---

## 2) Explicar el flujo completo (3 min)

**Qué decir:**
> "El flujo es: Pull Request → CI → merge a main → deploy automático a staging → aprobación manual → producción."

Muestra el diagrama verbalmente o dibuja:

```
PR → CI (lint+test+build) → merge a main → staging (auto-deploy) → aprobación manual → producción
```

**Archivos a mostrar:**
- [.github/workflows/ci.yml](.github/workflows/ci.yml) — se activa en cada PR y push a main.
- [.github/workflows/staging.yml](.github/workflows/staging.yml) — se activa solo en push a main.
- [.github/workflows/production.yml](.github/workflows/production.yml) — se activa manualmente (`workflow_dispatch`) y requiere aprobación del entorno `production`.

**Punto clave a remarcar:** ningún workflow despliega a producción automáticamente ni desde un PR.

---

## 3) Explicar feature flags (3 min)

**Qué decir:**
> "En vez de crear una rama larga para una funcionalidad grande, la desplegamos apagada por defecto y la activamos con una variable de entorno. Así se puede activar en staging, probarla, y luego en producción sin nuevo deploy."

**Archivos a mostrar:**
- [backend/feature_flags.py](backend/feature_flags.py) — lectura centralizada del flag en Python.
- [frontend/src/App.jsx](frontend/src/App.jsx) — lectura del flag en React (`import.meta.env.VITE_NEW_DASHBOARD_ENABLED`).
- [.env.example](.env.example) — dónde se documentan los flags disponibles.

Flag de ejemplo: `NEW_DASHBOARD_ENABLED` (por defecto `false`).

---

## 4) DEMO EN VIVO: hacer un cambio real (5-8 min)

Esta es la parte donde muestras el pipeline funcionando de verdad con un cambio pequeño y seguro.

### Paso 4.1 — Crear una rama

```powershell
git checkout -b demo/cambio-presentacion
```

### Paso 4.2 — Hacer un cambio visible y trivial

Ejemplo: cambiar un texto en el frontend. Abre [frontend/src/App.jsx](frontend/src/App.jsx) y cambia:

```jsx
<p>Este proyecto demuestra un pipeline CI/CD con feature flags seguros.</p>
```

por algo como:

```jsx
<p>Demo en vivo: este texto se actualizó para la presentación de hoy.</p>
```

**Qué decir mientras editas:**
> "Voy a hacer un cambio mínimo para mostrar cómo reacciona el pipeline, no el contenido en sí."

### Paso 4.3 — Verificar localmente antes de subir

```powershell
Set-Location 'C:\Users\IanSa\workflows\frontend'; npm test -- --run; npm run build
```

**Qué decir:**
> "Antes de subir cualquier cambio, corro las pruebas localmente. Esto es lo mismo que hará el pipeline, pero lo verifico primero para no depender solo de CI."

### Paso 4.4 — Commit y push

```powershell
git add .
git commit -m "demo: actualizar texto de presentacion"
git push origin demo/cambio-presentacion
```

### Paso 4.5 — Abrir el Pull Request

En GitHub, crea el PR hacia `main`.

**Qué mostrar en vivo:**
- El check de **CI** ejecutándose automáticamente en la pestaña **Checks** del PR.
- Explica: "Aquí se están instalando dependencias, corriendo lint, tests y build. Si algo falla, no puedo mergear."

### Paso 4.6 — Mergear el PR

Una vez CI está en verde, mergea a `main`.

**Qué mostrar:**
- Ve a la pestaña **Actions** y muestra que se disparó automáticamente el workflow **Staging deploy**.
- Explica: "Este workflow valida de nuevo y despliega a staging sin intervención humana."

### Paso 4.7 — Mostrar el intento de producción

Ve a **Actions → Production deploy → Run workflow**.

**Qué decir:**
> "La producción no se dispara sola. La ejecuto manualmente aquí, pero fíjense que GitHub va a pedir una aprobación antes de continuar, porque el entorno `production` tiene un revisor configurado."

Muestra la pantalla de **Review deployments** pidiendo aprobación.

---

## 5) DEMO: activar y desactivar el feature flag (3-5 min)

### Paso 5.1 — Activar el flag en staging

En GitHub → **Settings → Environments → staging → Environment variables**, agrega o edita:

```
NEW_DASHBOARD_ENABLED=true
```

**Qué decir:**
> "Sin tocar código ni hacer un nuevo deploy, activo esta variable y la próxima ejecución del pipeline en staging usará el nuevo comportamiento."

### Paso 5.2 — Mostrar el resultado

Vuelve a correr el workflow de staging (push vacío o re-run) y muestra el cambio de comportamiento (por ejemplo abriendo `frontend/src/App.jsx` localmente con la variable activada):

```powershell
$env:VITE_NEW_DASHBOARD_ENABLED = "true"
Set-Location 'C:\Users\IanSa\workflows\frontend'; npm run dev
```

### Paso 5.3 — Rollback rápido

**Qué decir:**
> "Si algo sale mal, no hago un revert de código. Solo cambio la variable de nuevo a `false` en el entorno. Eso es rollback inmediato."

```
NEW_DASHBOARD_ENABLED=false
```

---

## 6) Cierre y preguntas (2 min)

**Resumen para cerrar:**
> "Con este pipeline: nada llega a producción sin pasar CI, sin aprobación manual, y sin venir de `main`. Además, las funcionalidades nuevas se pueden activar o desactivar con una variable de entorno, sin necesidad de nuevos despliegues ni reverts de código."

**Preguntas frecuentes que te pueden hacer:**
- *"¿Qué pasa si el deploy a producción falla?"* → El workflow falla, no hay aprobación de un estado roto, y `concurrency` evita despliegues simultáneos que compliquen el diagnóstico.
- *"¿Dónde están los secretos?"* → Nunca en el código. Están en GitHub Secrets/Variables por entorno (ver [README.md](README.md)).
- *"¿Cómo agrego un flag nuevo?"* → Ver sección "Cómo agregar un nuevo feature flag" en [README.md](README.md).

---

## Checklist rápido para el día de la presentación

- [ ] Repo limpio, sin cambios sin commitear antes de empezar.
- [ ] Acceso abierto a GitHub Actions y Settings → Environments.
- [ ] Rama demo creada de antemano por si el live falla (`demo/cambio-presentacion`).
- [ ] Comando de verificación local copiado y probado.
- [ ] Saber de antemano si `production` tiene un aprobador configurado (tú mismo puedes serlo).
