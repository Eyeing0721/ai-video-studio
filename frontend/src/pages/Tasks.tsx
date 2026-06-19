import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

const API = 'http://127.0.0.1:8000'

interface TaskItem {
  id: string
  type: string
  status: string
  progress: number
  created_at: string
  error_message?: string
}

const STATUS: Record<string, { label: string; color: string }> = {
  pending: { label: '等待中', color: 'var(--theme-text-secondary)' },
  storyboarding: { label: '分镜中', color: 'var(--theme-accent)' },
  generating_images: { label: '生成图中', color: 'var(--theme-accent)' },
  generating_videos: { label: '生成视频中', color: 'var(--theme-accent)' },
  upscaling: { label: '超分中', color: 'var(--theme-accent)' },
  generating_audio: { label: '配音中', color: 'var(--theme-accent)' },
  compositing: { label: '合成中', color: 'var(--theme-accent)' },
  packaging: { label: '打包中', color: 'var(--theme-accent)' },
  completed: { label: '已完成', color: 'var(--theme-success)' },
  failed: { label: '失败', color: 'var(--theme-danger)' },
}

export default function Tasks() {
  const [tasks, setTasks] = useState<TaskItem[]>([])
  const nav = useNavigate()

  useEffect(() => {
    fetch(`${API}/api/tasks`)
      .then(r => r.json())
      .then(data => { if (Array.isArray(data)) setTasks(data) })
      .catch(() => {})
  }, [])

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6" style={{ color: 'var(--theme-text)' }}>任务列表</h1>
      {tasks.length === 0 ? (
        <p className="text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
          暂无任务，前往「一键成片」创建第一个任务。
        </p>
      ) : (
        <div className="space-y-3">
          {tasks.map((t) => {
            const s = STATUS[t.status] || { label: t.status, color: 'var(--theme-text-secondary)' }
            return (
              <button key={t.id} onClick={() => nav(`/tasks/${t.id}`)}
                className="w-full p-4 rounded-lg text-left flex items-center justify-between transition-all hover:scale-[1.01]"
                style={{ background: 'var(--theme-surface)', border: `1px solid var(--theme-border)`, borderRadius: 'var(--theme-radius-md)' }}>
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full flex items-center justify-center text-xs"
                    style={{ background: t.status === 'failed' ? 'var(--theme-danger)' : 'var(--theme-bg)' }}>
                    {t.status === 'completed' ? 'OK' : t.status === 'failed' ? 'X' : '...'}
                  </div>
                  <div>
                    <div className="font-medium text-sm" style={{ color: 'var(--theme-text)' }}>
                      {t.id.slice(0, 8)}... - {t.type === 'text' ? '文本创作' : '一键成片'}
                    </div>
                    <div className="text-xs mt-0.5" style={{ color: 'var(--theme-text-secondary)' }}>
                      {new Date(t.created_at).toLocaleString()}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  {!['completed', 'failed', 'pending'].includes(t.status) && (
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
      )}
    </div>
  )
}
