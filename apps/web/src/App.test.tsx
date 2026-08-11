/**
 * Module: App.test.tsx
 * Purpose: Verify semantic and honest baseline content.
 * Author: Kevin Cusnir with Codex
 * Date: 2026-08-11 (Asia/Jerusalem)
 */

import { render, screen } from '@testing-library/react'
import { describe, expect, it } from 'vitest'

import { App } from './App.tsx'

describe('App', () => {
  it('renders the Ezriva foundation without fake action controls', () => {
    render(<App />)

    expect(screen.getByRole('main')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: 'Ezriva' })).toBeInTheDocument()
    expect(screen.getByText('Clear help. Safe next steps.')).toBeInTheDocument()
    expect(screen.queryByRole('button', { hidden: true })).not.toBeInTheDocument()
  })
})
