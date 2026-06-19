import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

const API = 'http://127.0.0.1:8000'

type Mode = 'continue' | 'expand' | 'structured'

export default function TextCreation() {
  const [mode, setMode] = useState<Mode>('continue')
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [editInstruction, setEditInstruction] = useState('')
  const [loading, setLoading] = useState(false)
  const [length, setLength] = useState('3个段落')
  const [wordCount, setWordCount] = useState(2000)

  // Structured creation fields
  const [characters, setCharacters] = useState('')
  const [persona, setPersona] = useState('')
  const [world, setWorld] = useState('')
  const [style, setStyle] = useState('')
  const [plot, setPlot] = useState('')

  const nav = useNavigate()

  const callApi = async (endpoint: string, body: Record<string, unknown>) => {
    setLoading(true)
    try {
      const r = await fetch(`${API}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      const data = await r.json()
      if (data.text) setOutput(data.text)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleGenerate = async () => {
    switch (mode) {
      case 'continue':
        await callApi('/api/text/continue', { text: input, length })
        break
      case 'expand':
        await callApi('/api/text/expand', { sentence: input, word_count: wordCount })
        break
      case 'structured':
        await callApi('/api/text/structured', { characters, persona, world, style, plot, word_count: wordCount })
        break
    }
  }

  const handleRevise = () => {
    if (!output || !editInstruction) return
    callApi('/api/text/revise', { text: output, instruction: editInstruction })
  }

  return (
    <div className="max-w-4xl mx-auto h-full flex flex-col">
      <h1 className="text-2xl font-bold mb-4" style={{ color: 'var(--theme-text)' }}>文本创作</h1>

      <div className="flex gap-2 mb-4">
        {([
          ['continue', '续写'],
          ['expand', '一句话扩写'],
          ['structured', '结构化创作'],
        ] as [Mode, string][]).map(([m, label]) => (
          <button key={m} onClick={() => setMode(m)}
            className="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
            style={{
              background: mode === m ? 'var(--theme-accent)' : 'var(--theme-surface)',
              color: mode === m ? '#fff' : 'var(--theme-text)',
              border: `1px solid ${mode === m ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
              borderRadius: 'var(--theme-radius-md)',
            }}>
            {label}
          </button>
        ))}
      </div>

      <div className="flex-1 grid grid-cols-2 gap-4">
        <div className="flex flex-col gap-3">
          {mode === 'structured' ? (
            <>
              {[
                ['characters', '角色名称', '如"林小月, 25岁, 都市白领"'],
                ['persona', '角色人设（性格、背景、目标）', '如"内向但坚韧, 家庭压力大, 渴望自由"'],
                ['world', '世界观（修仙/科幻/都市/奇幻等）', '如"近未来赛博朋克都市"'],
                ['style', '风格（搞笑/悬疑/言情/热血等）', '如"悬疑+言情"'],
                ['plot', '剧情走向', '如"主角深入连环失踪案, 发现真相与自己有关"'],
              ].map(([key, label, placeholder]) => (
                <div key={key}>
                  <div className="text-xs font-medium mb-1" style={{ color: 'var(--theme-text-secondary)' }}>{label}</div>
                  <input placeholder={placeholder}
                    className="w-full px-3 py-2 rounded-lg text-sm"
                    style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}
                  />
                </div>
              ))}
              <div>
                <div className="text-xs font-medium mb-1" style={{ color: 'var(--theme-text-secondary)' }}>目标字数</div>
                <input type="number" value={wordCount} onChange={(e) => setWordCount(Number(e.target.value))}
                  className="w-full px-3 py-2 rounded-lg text-sm"
                  style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
              </div>
            </>
          ) : (
            <>
              <textarea value={input} onChange={(e) => setInput(e.target.value)}
                placeholder={mode === 'continue' ? '输入文本，系统自动续写...' : '输入一句话，系统自动扩写为完整故事...'}
                className="flex-1 p-4 resize-none text-sm rounded-lg" rows={10}
                style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
              {mode === 'continue' && (
                <div>
                  <label className="text-xs font-medium" style={{ color: 'var(--theme-text-secondary)' }}>续写长度</label>
                  <input value={length} onChange={(e) => setLength(e.target.value)}
                    className="w-full px-3 py-2 rounded-lg text-sm mt-1"
                    style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
                </div>
              )}
              {mode === 'expand' && (
                <div>
                  <label className="text-xs font-medium" style={{ color: 'var(--theme-text-secondary)' }}>目标字数</label>
                  <input type="number" value={wordCount} onChange={(e) => setWordCount(Number(e.target.value))}
                    className="w-full px-3 py-2 rounded-lg text-sm mt-1"
                    style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
                </div>
              )}
            </>
          )}
          <button onClick={handleGenerate} disabled={loading}
            className="py-2.5 rounded-lg text-sm font-medium text-white disabled:opacity-50"
            style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>
            {loading ? '生成中...' : '生成'}
          </button>
        </div>

        <div className="flex flex-col gap-3">
          <textarea value={output} onChange={(e) => setOutput(e.target.value)}
            className="flex-1 p-4 resize-none text-sm rounded-lg"
            style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}
            placeholder="生成结果..." />
          <div className="flex gap-2">
            <input value={editInstruction} onChange={(e) => setEditInstruction(e.target.value)}
              placeholder="输入修改指令，如「把主角改得更幽默」"
              className="flex-1 px-3 py-2 rounded-lg text-sm"
              style={{ background: 'var(--theme-bg)', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }} />
            <button onClick={handleRevise} disabled={loading}
              className="px-4 py-2 rounded-lg text-sm font-medium text-white"
              style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>
              修改
            </button>
          </div>
          <button onClick={() => output && nav(`/generate?text=${encodeURIComponent(output)}`)}
            className="py-2.5 rounded-lg text-sm font-medium text-white"
            style={{ background: 'var(--theme-success)', borderRadius: 'var(--theme-radius-md)' }}>
            送入视频生成
          </button>
        </div>
      </div>
    </div>
  )
}
