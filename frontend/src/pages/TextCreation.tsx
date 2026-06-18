import { useState } from 'react'

type Mode = 'continue' | 'expand' | 'structured'

export default function TextCreation() {
  const [mode, setMode] = useState<Mode>('continue')
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [editInstruction, setEditInstruction] = useState('')

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col">
      <h1 className="text-2xl font-bold mb-4" style={{ color: 'var(--theme-text)' }}>文本创作</h1>

      <div className="flex gap-2 mb-4">
        {([
          ['continue', '续写'],
          ['expand', '一句话扩写'],
          ['structured', '结构化创作'],
        ] as [Mode, string][]).map(([m, label]) => (
          <button
            key={m}
            onClick={() => setMode(m)}
            className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            style={{
              background: mode === m ? 'var(--theme-accent)' : 'var(--theme-surface)',
              color: mode === m ? '#fff' : 'var(--theme-text)',
              border: `1px solid ${mode === m ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            {label}
          </button>
        ))}
      </div>

      <div className="flex-1 grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-3">
          {mode === 'structured' ? (
            <>
              {[
                ['角色名称', 'characters'],
                ['角色人设（性格、背景、目标）', 'persona'],
                ['世界观（修仙/科幻/都市/奇幻等）', 'world'],
                ['风格（搞笑/悬疑/言情/热血等）', 'style'],
                ['剧情走向', 'plot'],
              ].map(([label, key]) => (
                <div key={key}>
                  <div className="text-xs font-medium mb-1" style={{ color: 'var(--theme-text-secondary)' }}>
                    {label}
                  </div>
                  <input
                    className="w-full px-3 py-2 rounded-lg text-sm"
                    style={{
                      background: 'var(--theme-bg)',
                      color: 'var(--theme-text)',
                      border: '1px solid var(--theme-border)',
                      borderRadius: 'var(--theme-radius-md)',
                    }}
                  />
                </div>
              ))}
            </>
          ) : (
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={mode === 'continue' ? '输入文本，系统自动续写...' : '输入一句话，系统自动扩写为完整故事...'}
              className="flex-1 p-4 resize-none text-sm rounded-lg"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
              rows={12}
            />
          )}
          <button
            className="py-2.5 rounded-lg text-sm font-medium text-white"
            style={{
              background: 'var(--theme-accent)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            生成
          </button>
        </div>

        <div className="flex flex-col gap-3">
          <textarea
            value={output}
            onChange={(e) => setOutput(e.target.value)}
            className="flex-1 p-4 resize-none text-sm rounded-lg font-mono"
            style={{
              background: 'var(--theme-bg)',
              color: 'var(--theme-text)',
              border: '1px solid var(--theme-border)',
              borderRadius: 'var(--theme-radius-md)',
            }}
            placeholder="生成结果..."
          />
          <div className="flex gap-2">
            <input
              value={editInstruction}
              onChange={(e) => setEditInstruction(e.target.value)}
              placeholder="输入修改指令，如「把主角改得更幽默」"
              className="flex-1 px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            />
            <button
              className="px-4 py-2 rounded-lg text-sm font-medium text-white"
              style={{
                background: 'var(--theme-accent)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              修改
            </button>
          </div>
          <button
            className="py-2.5 rounded-lg text-sm font-medium text-white"
            style={{
              background: 'var(--theme-success)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            送入视频生成
          </button>
        </div>
      </div>
    </div>
  )
}
