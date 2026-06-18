import { useNavigate } from 'react-router-dom'

const DEMO = [
  { id: '1', name: '修仙短剧第一集', status: 'completed', progress: 100, date: '2026-06-19 14:30' },
  { id: '2', name: '科幻悬疑片花', status: 'in_progress', progress: 67, date: '2026-06-19 16:00' },
  { id: '3', name: '旅行 Vlog', status: 'failed', progress: 45, date: '2026-06-18 22:15' },
]

const STATUS: Record<string, { label: string; color: string }> = {
  pending: { label: '等待中', color: 'var(--theme-text-secondary)' },
  in_progress: { label: '处理中', color: 'var(--theme-accent)' },
  completed: { label: '已完成', color: 'var(--theme-success)' },
  failed: { label: '失败', color: 'var(--theme-danger)' },
}

export default function Tasks() {
  const nav = useNavigate()

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6" style={{ color: 'var(--theme-text)' }}>任务列表</h1>
      <div className="space-y-3">
        {DEMO.map((t) => {
          const s = STATUS[t.status]
          return (
            <button
              key={t.id}
              onClick={() => nav(`/tasks/${t.id}`)}
              className="w-full p-4 rounded-lg text-left flex items-center justify-between transition-all hover:scale-[1.01]"
              style={{
                background: 'var(--theme-surface)',
                border: `1px solid var(--theme-border)`,
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-full flex items-center justify-center text-xs" style={{ background: 'var(--theme-bg)' }}>
                  {t.status === 'completed' ? 'V' : t.status === 'failed' ? 'X' : '...'}
                </div>
                <div>
                  <div className="font-medium text-sm" style={{ color: 'var(--theme-text)' }}>{t.name}</div>
                  <div className="text-xs mt-0.5" style={{ color: 'var(--theme-text-secondary)' }}>{t.date}</div>
                </div>
              </div>
              <div className="flex items-center gap-4">
                {t.status === 'in_progress' && (
                  <div className="w-24 h-1.5 rounded-full overflow-hidden" style={{ background: 'var(--theme-border)' }}>
                    <div className="h-full rounded-full transition-all" style={{ width: `${t.progress}%`, background: 'var(--theme-accent)' }} />
                  </div>
                )}
                <span className="text-xs font-medium" style={{ color: s.color }}>{s.label}</span>
              </div>
            </button>
          )
        })}
      </div>
    </div>
  )
}
