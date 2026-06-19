import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'

const API = 'http://127.0.0.1:8000'

interface Template {
  id: string
  name: string
  description: string
}

export default function Generate() {
  const [text, setText] = useState('')
  const [mode, setMode] = useState<'paste' | 'upload'>('paste')
  const [templates, setTemplates] = useState<Template[]>([])
  const [templateId, setTemplateId] = useState('micro_drama')
  const [resolution, setResolution] = useState('1080p')
  const [fps, setFps] = useState(24)
  const [maxDuration, setMaxDuration] = useState(120)
  const [voiceId, setVoiceId] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [fileName, setFileName] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const nav = useNavigate()

  useEffect(() => {
    fetch(`${API}/api/templates`)
      .then(r => r.json())
      .then(data => {
        if (Array.isArray(data)) {
          setTemplates(data)
          if (data.length > 0) setTemplateId(data[0].id)
        }
      })
      .catch(() => {/* backend not running yet */})
  }, [])

  const handleSubmit = async () => {
    if (!text.trim()) return
    setSubmitting(true)
    try {
      const r = await fetch(`${API}/api/tasks`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: 'generate',
          text: text.trim(),
          template: templateId,
          resolution,
          fps,
        }),
      })
      const data = await r.json()
      nav(`/tasks/${data.task_id}`)
    } catch (e) {
      console.error(e)
      setSubmitting(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6" style={{ color: 'var(--theme-text)' }}>一键成片</h1>

      <div className="space-y-5">
        <div className="flex gap-2">
          {(['paste', 'upload'] as const).map((m) => (
            <button key={m} onClick={() => setMode(m)} className="px-4 py-2 rounded-lg text-sm font-medium"
              style={{
                background: mode === m ? 'var(--theme-accent)' : 'var(--theme-surface)',
                color: mode === m ? '#fff' : 'var(--theme-text)',
                border: `1px solid ${mode === m ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
                borderRadius: 'var(--theme-radius-md)',
              }}>
              {m === 'paste' ? '粘贴文本' : '上传文件 (.txt/.md)'}
            </button>
          ))}
        </div>

        {mode === 'upload' ? (
          <>
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.md"
              className="hidden"
              onChange={(e) => {
                const file = e.target.files?.[0]
                if (!file) return
                setFileName(file.name)
                const reader = new FileReader()
                reader.onload = () => {
                  setText(reader.result as string)
                }
                reader.readAsText(file)
              }}
            />
            <div
              className="p-12 rounded-lg text-center border-2 border-dashed cursor-pointer hover:opacity-80 transition-opacity"
              style={{ background: 'var(--theme-bg)', borderColor: 'var(--theme-border)', borderRadius: 'var(--theme-radius-lg)' }}
              onClick={() => fileInputRef.current?.click()}
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => {
                e.preventDefault()
                const file = e.dataTransfer.files?.[0]
                if (!file) return
                if (!file.name.endsWith('.txt') && !file.name.endsWith('.md')) return
                setFileName(file.name)
                const reader = new FileReader()
                reader.onload = () => {
                  setText(reader.result as string)
                }
                reader.readAsText(file)
              }}
            >
              {fileName ? (
                <>
                  <p className="text-sm font-medium" style={{ color: 'var(--theme-text)' }}>{fileName}</p>
                  <p className="text-xs mt-1" style={{ color: 'var(--theme-text-secondary)' }}>点击重新选择，或切换到粘贴模式查看文本</p>
                </>
              ) : (
                <>
                  <p style={{ color: 'var(--theme-text-secondary)' }}>拖拽文件到此处，或点击选择</p>
                  <p className="text-xs mt-1" style={{ color: 'var(--theme-text-secondary)' }}>支持 .txt / .md</p>
                </>
              )}
            </div>
          </>
        ) : (
          <textarea value={text} onChange={(e) => setText(e.target.value)}
            placeholder="输入/粘贴小说文本或一句话描述..." className="w-full p-4 rounded-lg resize-none text-sm" rows={10}
            style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
        )}

        <div>
          <label className="text-xs font-medium mb-2 block" style={{ color: 'var(--theme-text-secondary)' }}>剪辑模板</label>
          <div className="grid grid-cols-3 gap-2">
            {templates.map((t) => (
              <button key={t.id} onClick={() => setTemplateId(t.id)}
                className="p-3 rounded-lg text-left text-sm transition-all"
                style={{
                  background: templateId === t.id ? 'var(--theme-accent)' : 'var(--theme-surface)',
                  color: templateId === t.id ? '#fff' : 'var(--theme-text)',
                  border: `1px solid ${templateId === t.id ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
                  borderRadius: 'var(--theme-radius-md)',
                }}>
                <div className="font-medium">{t.name}</div>
                <div className="text-xs mt-0.5 opacity-70">{t.description}</div>
              </button>
            ))}
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>分辨率</label>
            <select value={resolution} onChange={(e) => setResolution(e.target.value)}
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
              <option>720p</option><option>1080p</option><option>2K</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>帧率</label>
            <select value={fps} onChange={(e) => setFps(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
              <option value={24}>24fps</option><option value={30}>30fps</option><option value={60}>60fps</option>
            </select>
          </div>
          <div>
            <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>时长上限(秒)</label>
            <input type="number" value={maxDuration} onChange={(e) => setMaxDuration(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg text-sm"
              style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
          </div>
        </div>

        <div>
          <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
            音色（百炼音色 ID）
          </label>
          <input value={voiceId} onChange={(e) => setVoiceId(e.target.value)} placeholder="cosyvoice-v1"
            className="w-full px-3 py-2 rounded-lg text-sm"
            style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
        </div>

        <div>
          <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--theme-text-secondary)' }}>
            参考图（可选，约束角色/场景风格）
          </label>
          <div className="p-8 rounded-lg border-2 border-dashed text-center cursor-pointer"
            style={{ background: 'var(--theme-bg)', borderColor: 'var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
            <p className="text-sm" style={{ color: 'var(--theme-text-secondary)' }}>上传参考图（可多张）</p>
          </div>
        </div>

        <button onClick={handleSubmit} disabled={submitting}
          className="w-full py-3 rounded-xl text-base font-semibold text-white disabled:opacity-50"
          style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>
          {submitting ? '提交中...' : '开始生成'}
        </button>
      </div>
    </div>
  )
}
