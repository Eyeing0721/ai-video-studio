import { useState } from 'react'
import { Briefcase, Sparkles, FileText, MessageSquare, Loader2, Copy, Check, Download } from 'lucide-react'

const API = 'http://127.0.0.1:8000/api/career'

type Tab = 'full' | 'resume' | 'interview' | 'score'

export default function Career() {
  const [tab, setTab] = useState<Tab>('full')
  const [jd, setJd] = useState('')
  const [bg, setBg] = useState('')
  const [resume, setResume] = useState('')
  const [position, setPosition] = useState('')
  const [company, setCompany] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState('')
  const [copied, setCopied] = useState(false)

  const apiCall = async (endpoint: string, body: any) => {
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      setResult(data)
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleFullPackage = () => apiCall('/full-package', {
    job_description: jd, user_background: bg, target_position: position, company_name: company,
  })

  const handleResumeOnly = () => apiCall('/resume/optimize', {
    job_description: jd, user_background: bg, target_position: position,
  })

  const handleInterview = () => apiCall('/interview/full', {
    job_description: jd, interview_type: 'mixed', difficulty: 'medium',
  })

  const handleScore = () => apiCall('/resume/score', {
    resume, job_description: jd,
  })

  const copyText = (text: string) => {
    navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const downloadMd = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/markdown' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url; a.download = filename; a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <Briefcase /> AI 求职工具箱
      </h1>
      <p className="text-sm opacity-70">简历优化 · 模拟面试 · 求职全案 — 输入JD和背景，一键生成</p>

      {/* Tabs */}
      <div className="flex gap-2 flex-wrap">
        {([
          ['full', '一键全案'],
          ['resume', '简历优化'],
          ['interview', '模拟面试'],
          ['score', '简历评分'],
        ] as const).map(([key, label]) => (
          <button
            key={key}
            onClick={() => { setTab(key); setResult(null); setError('') }}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              tab === key ? 'text-white' : ''
            }`}
            style={{
              background: tab === key ? 'var(--theme-accent)' : 'var(--theme-surface)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <div className="glass-card p-6 space-y-4" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
        {tab === 'score' ? (
          <>
            <div>
              <label className="text-sm font-medium block mb-1">你的简历</label>
              <textarea
                className="w-full h-48 p-3 rounded-lg text-sm"
                style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                placeholder="粘贴你的简历内容..."
                value={resume}
                onChange={e => setResume(e.target.value)}
              />
            </div>
            <div>
              <label className="text-sm font-medium block mb-1">目标JD（可选，对比评分更准）</label>
              <textarea
                className="w-full h-32 p-3 rounded-lg text-sm"
                style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                placeholder="粘贴职位描述..."
                value={jd}
                onChange={e => setJd(e.target.value)}
              />
            </div>
            <button onClick={handleScore} disabled={loading || !resume} className="btn-primary flex items-center gap-2">
              {loading ? <Loader2 className="animate-spin" size={16} /> : <Sparkles size={16} />}
              评分
            </button>
          </>
        ) : (
          <>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium block mb-1">职位描述 (JD)</label>
                <textarea
                  className="w-full h-40 p-3 rounded-lg text-sm"
                  style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                  placeholder="粘贴目标岗位的招聘JD..."
                  value={jd}
                  onChange={e => setJd(e.target.value)}
                />
              </div>
              {tab !== 'interview' && (
                <div>
                  <label className="text-sm font-medium block mb-1">你的背景/原始简历</label>
                  <textarea
                    className="w-full h-40 p-3 rounded-lg text-sm"
                    style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                    placeholder="粘贴你的工作经历、项目经验、教育背景...越详细效果越好"
                    value={bg}
                    onChange={e => setBg(e.target.value)}
                  />
                </div>
              )}
            </div>
            <div className="grid grid-cols-3 gap-4">
              <input
                className="p-2.5 rounded-lg text-sm"
                style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                placeholder="目标岗位名称（可选）"
                value={position}
                onChange={e => setPosition(e.target.value)}
              />
              <input
                className="p-2.5 rounded-lg text-sm"
                style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}
                placeholder="目标公司（可选）"
                value={company}
                onChange={e => setCompany(e.target.value)}
              />
              <button
                onClick={
                  tab === 'full' ? handleFullPackage :
                  tab === 'resume' ? handleResumeOnly :
                  handleInterview
                }
                disabled={loading || !jd || (tab !== 'interview' && !bg)}
                className="btn-primary flex items-center justify-center gap-2"
              >
                {loading ? <Loader2 className="animate-spin" size={16} /> : <Sparkles size={16} />}
                {tab === 'full' ? '一键生成全案' : tab === 'resume' ? '优化简历' : '生成面试题'}
              </button>
            </div>
          </>
        )}
      </div>

      {error && (
        <div className="p-4 rounded-lg text-red-400" style={{ background: 'var(--theme-surface)' }}>
          {error}
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {result.resume && (
            <div className="glass-card p-6" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-bold flex items-center gap-2"><FileText size={18} /> 优化后简历</h2>
                <div className="flex gap-2">
                  <button onClick={() => copyText(result.resume)} className="btn-ghost text-sm flex items-center gap-1">
                    {copied ? <Check size={14} /> : <Copy size={14} />} 复制
                  </button>
                  <button onClick={() => downloadMd(result.resume, 'resume.md')} className="btn-ghost text-sm flex items-center gap-1">
                    <Download size={14} /> 下载
                  </button>
                </div>
              </div>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans p-4 rounded-lg" style={{ background: 'var(--theme-surface)' }}>
                {result.resume}
              </pre>
            </div>
          )}

          {result.cover_letter && (
            <div className="glass-card p-6" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
              <h2 className="text-lg font-bold mb-3 flex items-center gap-2"><MessageSquare size={18} /> 求职信</h2>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans p-4 rounded-lg" style={{ background: 'var(--theme-surface)' }}>
                {result.cover_letter}
              </pre>
            </div>
          )}

          {result.mock_interview && (
            <div className="glass-card p-6" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
              <h2 className="text-lg font-bold mb-3">模拟面试</h2>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans p-4 rounded-lg" style={{ background: 'var(--theme-surface)', maxHeight: 400, overflow: 'auto' }}>
                {JSON.stringify(result.mock_interview, null, 2)}
              </pre>
            </div>
          )}

          {result.resume_score && (
            <div className="glass-card p-6" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
              <h2 className="text-lg font-bold mb-3">简历评分</h2>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans p-4 rounded-lg" style={{ background: 'var(--theme-surface)', maxHeight: 400, overflow: 'auto' }}>
                {JSON.stringify(result.resume_score, null, 2)}
              </pre>
            </div>
          )}

          {/* Score-only result */}
          {result.overall_score !== undefined && (
            <div className="glass-card p-6" style={{ borderRadius: 'var(--theme-radius-lg)' }}>
              <h2 className="text-lg font-bold mb-3">评分结果</h2>
              <div className="text-4xl font-bold mb-4" style={{ color: 'var(--theme-accent)' }}>
                {result.overall_score} / 10
              </div>
              <pre className="whitespace-pre-wrap text-sm leading-relaxed font-sans p-4 rounded-lg" style={{ background: 'var(--theme-surface)' }}>
                {JSON.stringify(result, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
