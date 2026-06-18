import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Generate() {
  const [text, setText] = useState('')
  const [mode, setMode] = useState<'paste' | 'upload'>('paste')
  const nav = useNavigate()

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6" style={{ color: 'var(--theme-text)' }}>一键成片</h1>

      <div className="space-y-5">
        <div className="flex gap-2">
          {(['paste', 'upload'] as const).map((m) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className="px-4 py-2 rounded-lg text-sm font-medium"
              style={{
                background: mode === m ? 'var(--theme-accent)' : 'var(--theme-surface)',
                color: mode === m ? '#fff' : 'var(--theme-text)',
                border: `1px solid ${mode === m ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              {m === 'paste' ? '粘贴文本' : '上传文件 (.txt/.md)'}
            </button>
          ))}
        </div>

        {mode === 'upload' ? (
          <div
            className="p-12 rounded-lg text-center border-2 border-dashed cursor-pointer"
            style={{
              background: 'var(--theme-bg)',
              borderColor: 'var(--theme-border)',
              borderRadius: 'var(--theme-radius-lg)',
            }}
          >
            <p style={{ color: 'var(--theme-text-secondary)' }}>拖拽文件到此处，或点击选择</p>
            <p className="text-xs mt-1" style={{ color: 'var(--theme-text-secondary)' }}>
              支持 .txt / .md
            </p>
          </div>
        ) : (
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="输入/粘贴小说文本或一句话描述..."
            className="w-full p-4 rounded-lg resize-none text-sm"
            rows={10}
            style={{
              background: 'var(--theme-bg)',
              color: 'var(--theme-text)',
              border: '1px solid var(--theme-border)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          />
        )}

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
              分辨率
            </label>
            <select
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              <option>1080p</option>
              <option>720p</option>
              <option>2K</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
              帧率
            </label>
            <select
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              <option>24fps</option>
              <option>30fps</option>
              <option>60fps</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
              时长上限（秒）
            </label>
            <input
              type="number"
              defaultValue={120}
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
              音色（百炼音色 ID 或上传音频克隆）
            </label>
            <input
              placeholder="cosyvoice-xxx"
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            />
          </div>
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
              BGM
            </label>
            <select
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              <option>自动选择</option>
              <option>无 BGM</option>
              <option>从资产库选择</option>
            </select>
          </div>
        </div>

        <div>
          <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
            参考图（可选，约束角色/场景风格）
          </label>
          <div
            className="p-8 rounded-lg border-2 border-dashed text-center cursor-pointer"
            style={{
              background: 'var(--theme-bg)',
              borderColor: 'var(--theme-border)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            <p className="text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
              上传参考图（可多张）
            </p>
          </div>
        </div>

        <button
          onClick={() => nav('/tasks')}
          className="w-full py-3 rounded-xl text-base font-semibold text-white"
          style={{
            background: 'var(--theme-accent)',
            borderRadius: 'var(--theme-radius-md)',
          }}
        >
          开始生成
        </button>
      </div>
    </div>
  )
}
