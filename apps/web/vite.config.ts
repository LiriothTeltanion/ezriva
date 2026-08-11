/**
 * Module: vite.config.ts
 * Purpose: Configure the Ezriva web build and isolated component tests.
 * Author: Kevin Cusnir with Codex
 * Date: 2026-08-11 (Asia/Jerusalem)
 */

import react from '@vitejs/plugin-react'
import { defineConfig } from 'vitest/config'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
  },
})
