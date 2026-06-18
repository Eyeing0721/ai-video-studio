import { useNavigate } from 'react-router-dom'
import { FileText, Film } from 'lucide-react'

export default function Home() {
  const nav = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center h-full gap-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2" style={{ color: 'var(--theme-text)' }}>
          AI Video Studio
        </h1>
        <p className="text-lg" style={{ color: 'var(--theme-text-secondary)' }}>
          从文本到成片，全自动 AI 视频生成工作台
        </p>
      </div>
      <div className="flex gap-6">
        <button
          onClick={() => nav('/text')}
          className="flex flex-col items-center gap-4 p-8 rounded-2xl w-56 transition-all hover:scale-105"
          style={{
            background: 'var(--theme-surface)',
            border: `1px solid var(--theme-border)`,
            borderRadius: 'var(--theme-radius-lg)',
          }}
        >
          <FileText size={40} style={{ color: 'var(--theme-accent)' }} />
          <span className="text-lg font-semibold" style={{ color: 'var(--theme-text)' }}>
            文本创作
          </span>
          <span className="text-sm text-center" style={{ color: 'var(--theme-text-secondary)' }}>
            续写、扩写、结构化创作，先生成小说再进流水线
          </span>
        </button>
        <button
          onClick={() => nav('/generate')}
          className="flex flex-col items-center gap-4 p-8 rounded-2xl w-56 transition-all hover:scale-105"
          style={{
            background: 'var(--theme-surface)',
            border: `1px solid var(--theme-border)`,
            borderRadius: 'var(--theme-radius-lg)',
          }}
        >
          <Film size={40} style={{ color: 'var(--theme-accent)' }} />
          <span className="text-lg font-semibold" style={{ color: 'var(--theme-text)' }}>
            一键成片
          </span>
          <span className="text-sm text-center" style={{ color: 'var(--theme-text-secondary)' }}>
            直接输入文本/小说，全自动分镜到成片
          </span>
        </button>
      </div>
    </div>
  )
}
