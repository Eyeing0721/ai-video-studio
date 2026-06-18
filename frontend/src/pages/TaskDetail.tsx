import { useParams } from 'react-router-dom'

const STEPS = [
  { key: 'storyboarding', label: '分镜拆解', status: 'done' },
  { key: 'generating_images', label: '静态图生成 (3/4)', status: 'in_progress' },
  { key: 'generating_videos', label: '图生视频', status: 'pending' },
  { key: 'upscaling', label: '超分', status: 'pending' },
  { key: 'generating_audio', label: '配音', status: 'pending' },
  { key: 'compositing', label: '后期合成', status: 'pending' },
]

const LOGS = [
  '[14:30:02] 任务创建, ID: task-001',
  '[14:30:03] 文本分析完成, 拆解为 4 个分镜',
  '[14:30:05] 分镜 1 关键帧生成中... (Z-Image Turbo, 1024x1024)',
  '[14:30:28] 分镜 1 关键帧完成',
  '[14:30:30] 分镜 2 关键帧生成中...',
]

export default function TaskDetail() {
  const { id } = useParams()

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-full">
      <h1 className="text-2xl font-bold mb-2" style={{ color: 'var(--theme-text)' }}>
        任务 {id}
      </h1>
      <p className="text-sm mb-6" style={{ color: 'var(--theme-text-secondary)' }}>修仙短剧第一集</p>

      <div className="flex-1 grid grid-cols-5 gap-6">
        <div className="col-span-3 space-y-4">
          {STEPS.map((s, i) => (
            <div
              key={s.key}
              className="flex items-center gap-4 p-3 rounded-lg"
              style={{
                background: s.status === 'in_progress' ? 'var(--theme-bg)' : 'var(--theme-surface)',
                border: `1px solid ${s.status === 'in_progress' ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
                borderRadius: 'var(--theme-radius-md)',
                opacity: s.status === 'pending' ? 0.5 : 1,
              }}
            >
              <div
                className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white shrink-0"
                style={{
                  background:
                    s.status === 'done' ? 'var(--theme-success)' :
                    s.status === 'in_progress' ? 'var(--theme-accent)' :
                    'var(--theme-border)',
                }}
              >
                {s.status === 'done' ? 'OK' : i + 1}
              </div>
              <span className="text-sm font-medium" style={{ color: 'var(--theme-text)' }}>{s.label}</span>
              {s.status === 'in_progress' && (
                <div className="ml-auto w-16 h-1 rounded-full overflow-hidden" style={{ background: 'var(--theme-border)' }}>
                  <div className="h-full rounded-full animate-pulse" style={{ width: '60%', background: 'var(--theme-accent)' }} />
                </div>
              )}
            </div>
          ))}
        </div>

        <div className="col-span-2">
          <div
            className="p-4 rounded-lg h-full overflow-auto"
            style={{
              background: '#0D0E12',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            <div className="text-xs text-green-400 font-mono space-y-1">
              {LOGS.map((l, i) => (
                <div key={i}>{l}</div>
              ))}
              <div className="text-green-400 animate-pulse">|</div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex gap-3 mt-6 pb-6">
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium text-white"
          style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}
        >
          下载成片
        </button>
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium"
          style={{ background: 'transparent', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}
        >
          下载中间资产 ZIP
        </button>
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium"
          style={{ background: 'transparent', color: 'var(--theme-danger)', border: '1px solid var(--theme-danger)', borderRadius: 'var(--theme-radius-md)' }}
        >
          重新生成
        </button>
      </div>
    </div>
  )
}
