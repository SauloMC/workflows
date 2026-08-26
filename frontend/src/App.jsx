export default function App() {
  const isNewDashboardEnabled = import.meta.env.VITE_NEW_DASHBOARD_ENABLED === 'true'

  return (
    <main className="app-shell">
      <h1>Workflow Demo</h1>
      <p>Este proyecto demuestrasdfasdfaaasdsa un pipeline CI/CD con feature flags seguros.</p>

      {isNewDashboardEnabled ? (
        <section className="card feature-enabled">
          <h2>Nuevo dashboard habilitado</h2>
          <p>La funcionalidad nueva está activa en este entorno.</p>
        </section>
      ) : (
        <section className="card feature-disabled">
          <h2>Dashboard clásico</h2>
          <p>La funcionalidad nueva sigue apagada por defecto.</p>
        </section>
      )}
    </main>
  )
}
