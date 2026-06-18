const TYPES = ['全部', 'BGM', '转场', '字幕', 'LUT', 'SFX'] as const

const DEMO = [
  { type: 'BGM', name: 'Gentle Morning', tags: ['温暖', '钢琴', '慢节奏'], duration: '2:30' },
  { type: 'BGM', name: 'Cyber Chase', tags: ['电子', '快节奏', '悬疑'], duration: '1:45' },
  { type: 'BGM', name: 'Sakura Tears', tags: ['弦乐', '情感', '日本'], duration: '3:10' },
  { type: '转场', name: 'Smooth Slide', tags: ['滑动', '商务', '柔滑'], duration: '-' },
  { type: '字幕', name: '简约白字', tags: ['白色', '无衬线', '描边'], duration: '-' },
  { type: 'LUT', name: 'Teal & Orange', tags: ['电影感', '暖色', '高对比'], duration: '-' },
]

export default function Assets() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold" style={{ color: 'var(--theme-text)' }}>资产库</h1>
        <button
          className="px-4 py-2 rounded-lg text-sm font-medium text-white"
          style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}
        >
          上传资产
        </button>
      </div>

      <div className="flex gap-2 mb-4">
        <input
          placeholder="搜索标签..."
          className="flex-1 px-3 py-2 rounded-lg text-sm"
          style={{
            background: 'var(--theme-bg)',
            color: 'var(--theme-text)',
            border: '1px solid var(--theme-border)',
            borderRadius: 'var(--theme-radius-md)',
          }}
        />
      </div>

      <div className="flex gap-2 mb-6">
        {TYPES.map((t) => (
          <button
            key={t}
            className="px-3 py-1.5 rounded-lg text-xs font-medium"
            style={{
              background: t === '全部' ? 'var(--theme-accent)' : 'var(--theme-surface)',
              color: t === '全部' ? '#fff' : 'var(--theme-text)',
              border: `1px solid ${t === '全部' ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
              borderRadius: 'var(--theme-radius-sm)',
            }}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-3">
        {DEMO.map((a, i) => (
          <div
            key={i}
            className="p-4 rounded-lg"
            style={{
              background: 'var(--theme-surface)',
              border: '1px solid var(--theme-border)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs px-2 py-0.5 rounded font-medium" style={{ background: 'var(--theme-bg)', color: 'var(--theme-accent)' }}>
                {a.type}
              </span>
              <span className="text-xs" style={{ color: 'var(--theme-text-secondary)' }}>{a.duration}</span>
            </div>
            <div className="font-medium text-sm mb-2" style={{ color: 'var(--theme-text)' }}>{a.name}</div>
            <div className="flex gap-1.5 flex-wrap">
              {a.tags.map((t) => (
                <span
                  key={t}
                  className="text-xs px-2 py-0.5 rounded-full"
                  style={{
                    background: 'var(--theme-bg)',
                    color: 'var(--theme-text-secondary)',
                  }}
                >
                  {t}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
