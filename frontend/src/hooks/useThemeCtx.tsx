import { createContext, useContext } from 'react'
import { useTheme } from './useTheme'
import type { ThemeConfig, ThemePreset } from '../types/theme'

interface ThemeCtx {
  preset: ThemePreset
  config: ThemeConfig
  switchPreset: (p: ThemePreset) => void
  updateCustom: (c: ThemeConfig) => void
  exportTheme: () => string
  importTheme: (json: string) => void
}

const ThemeContext = createContext<ThemeCtx | null>(null)

// eslint-disable-next-line react-refresh/only-export-components
export function useThemeCtx() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useThemeCtx must be inside ThemeProvider')
  return ctx
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useTheme()
  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
}
