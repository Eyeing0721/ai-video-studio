import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './hooks/useThemeCtx'
import Layout from './components/Layout'
import ThemeWizard from './components/ThemeWizard'
import SetupWizard from './components/SetupWizard'
import Home from './pages/Home'
import TextCreation from './pages/TextCreation'
import Generate from './pages/Generate'
import Tasks from './pages/Tasks'
import TaskDetail from './pages/TaskDetail'
import Assets from './pages/Assets'
import Settings from './pages/Settings'

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <ThemeWizard />
        <SetupWizard onDone={() => {}} />
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
