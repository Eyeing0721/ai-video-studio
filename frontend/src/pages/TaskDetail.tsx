import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import useWebSocket from '../hooks/useWebSocket'

const API = 'http://127.0.0.1:8000'

interface ShotData {
  id: number
  shot_index: number
  description: string
  dialogue: string
  mood: string
  duration_sec: number
  status: string
}

interface TaskData {
  id: string
  status: string
  progress: number
  resolution: string
  fps: number
  storyboard: Array<Record<string, unknown>>
  shots: ShotData[]
  error_message?: string
  recipe?: Record<string, unknown>
}

const STEP_MAP: Record<string, { label: string; order: number }> = {
  pending: { label: '等待中', order: 0 },
  storyboarding: { label: '分镜拆解', order: 1 },
  generating_images: { label: '静态图生成', order: 2 },
  generating_videos: { label: '图生视频', order: 3 },
  upscaling: { label: '超分辨率', order: 4 },
  generating_audio: { label: '配音生成', order: 5 },
  compositing: { label: '后期合成', order: 6 },
  packaging: { label: '资产打包', order: 7 },
  completed: { label: '完成', order: 8 },
}

const ALL_STEPS = Object.entries(STEP_MAP)
  .filter(([, v]) => v.order > 0 && v.order < 8)
  .sort((a, b) => a[1].order - b[1].order)

export default function TaskDetail() {
  const { id } = useParams()
  const [task, setTask] = useState<TaskData | null>(null)
  const [logs, setLogs] = useState<string[]>([])

  const { connected } = useWebSocket({
    taskId: id!,
    onMessage: (msg) => {
      if (msg.type === 'status') {
        setTask((prev) => prev ? { ...prev, status: msg.status as string, progress: msg.progress as number } : prev)
        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] ${msg.label} (${Math.round(msg.progress as number)}%)`])
      } else if (msg.type === 'completed') {
        setTask((prev) => prev ? { ...prev, status: 'completed', progress: 100 } : prev)
        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 任务完成`])
      } else if (msg.type === 'failed') {
        setTask((prev) => prev ? { ...prev, status: 'failed' } : prev)
        setLogs((prev) => [...prev, `[${new Date().toLocaleTimeString()}] 失败: ${msg.error}`])
      }
    },
  })

  useEffect(() => {
    fetch(`${API}/api/tasks/${id}`)
      .then(r => r.json())
      .then(data => {
        if (data.id) setTask(data)
      })
      .catch(() => {})
  }, [id])

  if (!task) return <p style={{ color: 'var(--theme-text-secondary)' }}>加载中...</p>

  const currentOrder = STEP_MAP[task.status]?.order ?? 0

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-full">
      <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--theme-text)' }}>
        任务 {id?.slice(0, 8)}
      </h1>
      <div className="flex gap-4 mb-6 text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
        <span>{task.resolution} / {task.fps}fps</span>
        <span>{task.shots?.length || 0} 个分镜</span>
        <span>进度: {Math.round(task.progress)}%</span>
      </div>

      <div className="flex-1 grid grid-cols-5 gap-6">
        <div className="col-span-3 space-y-4">
          {ALL_STEPS.map(([key, { label, order }]) => {
            const isDone = currentOrder > order || task.status === 'completed'
            const isCurrent = currentOrder === order
            const isPending = currentOrder < order

            return (
              <div key={key}
                className="flex items-center gap-4 p-3 rounded-lg"
                style={{
                  background: isCurrent ? 'var(--theme-bg)' : 'var(--theme-surface)',
                  border: `1px solid ${isCurrent ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
                  borderRadius: 'var(--theme-radius-md)',
                  opacity: isPending ? 0.4 : 1,
                }}>
                <div className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
                  style={{ background: isDone ? 'var(--theme-success)' : isCurrent ? 'var(--theme-accent)' : 'var(--theme-border)' }}>
                  {isDone ? 'OK' : order}
                </div>
                <span className="text-sm font-medium" style={{ color: 'var(--theme-text)' }}>{label}</span>
                {isCurrent && task.status !== 'completed' && (
                  <div className="ml-auto w-20 h-1 rounded-full overflow-hidden" style={{ background: 'var(--theme-border)' }}>
                    <div className="h-full rounded-full animate-pulse" style={{ width: '60%', background: 'var(--theme-accent)' }} />
                  </div>
                )}
              </div>
            )
          })}

          {task.status === 'failed' && (
            <div className="p-4 rounded-lg" style={{ background: 'var(--theme-danger)', color: '#fff', borderRadius: 'var(--theme-radius-md)' }}>
              <div className="font-medium text-sm">任务失败</div>
              <div className="text-xs mt-1">{task.error_message || '未知错误'}</div>
            </div>
          )}
        </div>

        <div className="col-span-2">
          <div className="p-4 rounded-lg h-full overflow-auto text-xs font-mono"
            style={{ background: '#0D0E12', borderRadius: 'var(--theme-radius-md)' }}>
            {logs.length === 0 ? (
              <div style={{ color: '#666' }}>等待日志...</div>
            ) : (
              logs.map((l, i) => (
                <div key={i} style={{ color: '#4ade80' }}>{l}</div>
              ))
            )}
            {task.status !== 'completed' && task.status !== 'failed' && (
              <div className="animate-pulse" style={{ color: '#4ade80' }}>|</div>
            )}
          </div>
        </div>
      </div>

      <div className="flex gap-3 mt-6 pb-6">
        {task.status === 'completed' && (
          <button className="px-4 py-2 rounded-lg text-sm font-medium text-white"
            style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>
            下载成片
          </button>
        )}
        <button className="px-4 py-2 rounded-lg text-sm font-medium"
          style={{ background: 'transparent', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
          下载中间资产 ZIP
        </button>
        {task.status === 'failed' && (
          <button className="px-4 py-2 rounded-lg text-sm font-medium"
            style={{ background: 'transparent', color: 'var(--theme-danger)', border: '1px solid var(--theme-danger)', borderRadius: 'var(--theme-radius-md)' }}>
            重新生成
          </button>
        )}
      </div>
    </div>
  )
}
