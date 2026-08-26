import { describe, expect, it, vi, afterEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

afterEach(() => {
  vi.unstubAllEnvs()
})

describe('App feature flag rendering', () => {
  it('shows classic dashboard when flag is off', () => {
    vi.stubEnv('VITE_NEW_DASHBOARD_ENABLED', 'false')

    render(<App />)
    expect(screen.getByText('Dashboard clásico')).toBeTruthy()
  })

  it('shows new dashboard when flag is on', () => {
    vi.stubEnv('VITE_NEW_DASHBOARD_ENABLED', 'true')

    render(<App />)
    expect(screen.getByText('Nuevo dashboard habilitado')).toBeTruthy()
  })
})
