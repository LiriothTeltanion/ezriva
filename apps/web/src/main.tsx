/**
 * Module: main.tsx
 * Purpose: Mount the accessible Ezriva web foundation.
 * Author: Kevin Cusnir with Codex
 * Date: 2026-08-11 (Asia/Jerusalem)
 */

import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import { App } from './App.tsx'
import './styles.css'

const rootElement = document.querySelector<HTMLElement>('#root')

if (rootElement === null) {
  throw new Error('Ezriva could not find the #root mount element.')
}

createRoot(rootElement).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
