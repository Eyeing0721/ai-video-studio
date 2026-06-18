import { createContext, useContext } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useTheme } from './hooks/useTheme'
import type { ThemeConfig, ThemePreset } from './types/theme'
import Layout from './components/Layout'
import ThemeWizard from './components/ThemeWizard'
import Home from './pages/Home'
import TextCreation from './pages/TextCreation'
import Generate from './pages/Generate'
import Tasks from './pages/Tasks'
import TaskDetail from './pages/TaskDetail'
import Assets from './pages/Assets'
import Settings from './pages/Settings'

interface ThemeCtx {
  preset: ThemePreset
  config: ThemeConfig
  switchPreset: (p: ThemePreset) => void
  updateCustom: (c: ThemeConfig) => void
  exportTheme: () => string
  importTheme: (json: string) => void
}

const ThemeContext = createContext<ThemeCtx | null>(null)

export function useThemeCtx() {
  const ctx = useContext(ThemeContext)
  if (!ctx) throw new Error('useThemeCtx must be inside ThemeProvider')
  return ctx
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const theme = useTheme()
  return <ThemeContext.Provider value={theme}>{children}</ThemeContext.Provider>
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <ThemeWizard />
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<Home />} />
            <Route path="/text" element={<TextCreation />} />
            <Route path="/generate" element={<Generate />} />
            <Route path="/tasks" element={<Tasks />} />
            <Route path="/tasks/:id" element={<TaskDetail />} />
            <Route path="/assets" element={<Assets />} />
            <Route path="/settings" element={<Settings />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}
