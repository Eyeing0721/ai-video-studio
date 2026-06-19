import { Outlet, NavLink, useLocation } from 'react-router-dom'
import { Film, FileText, ListTodo, FolderOpen, Settings } from 'lucide-react'

const NAV = [
  { to: '/', label: '首页', icon: Film },
  { to: '/text', label: '文本创作', icon: FileText },
  { to: '/generate', label: '一键成片', icon: Film },
  { to: '/tasks', label: '任务', icon: ListTodo },
  { to: '/assets', label: '资产库', icon: FolderOpen },
  { to: '/settings', label: '设置', icon: Settings },
]

export default function Layout() {
  const location = useLocation()
  return (
    <div className="flex h-screen" style={{ background: 'var(--theme-bg)' }}>
      <nav className="w-56 shrink-0 flex flex-col gap-1 p-4 glass"
        style={{ borderColor: 'var(--theme-border)' }}
      >
        <div className="text-lg font-bold tracking-tight mb-6 px-2" style={{ color: 'var(--theme-accent)' }}>
          AI Video Studio
        </div>
        {NAV.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive ? '' : ''
              }`
            }
            style={({ isActive }) => ({
              background: isActive ? 'var(--theme-accent)' : 'transparent',
              color: isActive ? '#fff' : 'var(--theme-text)',
              borderRadius: 'var(--theme-radius-md)',
            })}
          >
            <Icon size={18} />
            {label}
          </NavLink>
        ))}
      </nav>
      <main className="flex-1 overflow-auto p-6">
        <div className="page-enter" key={location.pathname}>
          <Outlet />
        </div>
      </main>
    </div>
  )
}
