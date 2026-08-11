/**
 * Module: App.tsx
 * Purpose: Show an honest, semantic foundation screen before the hero flow exists.
 * Author: Kevin Cusnir with Codex
 * Date: 2026-08-11 (Asia/Jerusalem)
 */

import type { ReactElement } from 'react'

export function App(): ReactElement {
  return (
    <main className="foundation" aria-labelledby="product-name">
      <p className="eyebrow">Agents for Humans Hackathon</p>
      <h1 id="product-name">Ezriva</h1>
      <p className="tagline">Clear help. Safe next steps.</p>
      <section aria-labelledby="build-status" className="status-card">
        <h2 id="build-status">Foundation only</h2>
        <p>
          The agent workflow is not active yet. Hebrew understanding, human approval,
          and real reminder actions will appear only after their safety checks pass.
        </p>
      </section>
    </main>
  )
}
