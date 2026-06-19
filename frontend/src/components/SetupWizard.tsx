import { useState, useEffect } from 'react'
import { Check, X, Loader2, Download, ExternalLink } from 'lucide-react'

const API = 'http://127.0.0.1:8000'

interface CheckItem {
  key: string
  label: string
  status: 'pending' | 'checking' | 'ok' | 'error'
  detail: string
  action?: { label: string; url: string }
}

export default function SetupWizard({ onDone }: { onDone: () => void }) {
  const [show, setShow] = useState(() => {
    const setupDone = localStorage.getItem('avs-setup-done')
    const themeDone = localStorage.getItem('ai-video-studio-wizard-done')
    return !setupDone && !!themeDone
  })
  const [checks, setChecks] = useState<CheckItem[]>([])
  const [overall, setOverall] = useState<'checking' | 'ready' | 'blocked'>('checking')

  useEffect(() => {
    if (show) runChecks()
  }, [show])

  if (!show) return null

  const runChecks = async () => {
    const items: CheckItem[] = [
      { key: 'comfyui', label: 'ComfyUI 服务', status: 'pending', detail: '' },
      { key: 'ffmpeg', label: 'FFmpeg', status: 'pending', detail: '' },
      { key: 'models_zimage', label: 'Z-Image 模型', status: 'pending', detail: '' },
      { key: 'models_wan', label: 'Wan 2.2 模型', status: 'pending', detail: '' },
      { key: 'models_sulphur', label: 'Sulphur 2 模型', status: 'pending', detail: '' },
      { key: 'disk_space', label: '磁盘空间', status: 'pending', detail: '' },
      { key: 'deepseek_key', label: 'DeepSeek API Key', status: 'pending', detail: '' },
    ]
    setChecks(items)

    try {
      const r = await fetch(`${API}/api/health/detailed`)
      const data = await r.json()

      const updated = items.map(item => {
        const health = data[item.key] || data[item.key.replace('models_', '')]
        if (item.key === 'comfyui') {
          const h = data.comfyui
          if (h?.status === 'ok') return { ...item, status: 'ok' as const, detail: h.detail || '已连接' }
          return { ...item, status: 'error' as const, detail: h?.detail || '无法连接',
            action: { label: '如何安装 ComfyUI', url: 'https://docs.comfy.org/install' } }
        }
        if (item.key === 'ffmpeg') {
          return data.ffmpeg ? { ...item, status: 'ok' as const, detail: '已安装' }
            : { ...item, status: 'error' as const, detail: '未找到', action: { label: '下载 FFmpeg', url: 'https://ffmpeg.org/download.html' } }
        }
        if (item.key === 'disk_space') {
          const gb = data.disk_space_gb || 0
          return gb >= 50 ? { ...item, status: 'ok' as const, detail: `${gb}GB 可用` }
            : { ...item, status: 'error' as const, detail: `仅 ${gb}GB，建议 50GB+` }
        }
        if (item.key === 'deepseek_key') {
          return data.deepseek_api ? { ...item, status: 'ok' as const, detail: '已配置' }
            : { ...item, status: 'error' as const, detail: '未配置', action: { label: '获取 API Key', url: 'https://platform.deepseek.com/api_keys' } }
        }
        if (item.key.startsWith('models_')) {
          const MODEL_MAP: Record<string, string> = {
            models_zimage: 'z_image',
            models_wan: 'wan_i2v_high',
            models_sulphur: 'sulphur_fp8',
          }
          const realKey = MODEL_MAP[item.key] || item.key.replace('models_', '')
          const models = data.models || {}
          const ok = models[realKey] === true
          return ok ? { ...item, status: 'ok' as const, detail: '模型文件存在' }
            : { ...item, status: 'error' as const, detail: '模型文件缺失',
              action: { label: '下载指引', url: 'https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged' } }
        }
        return { ...item, status: 'ok' as const, detail: '正常' }
      })

      setChecks(updated)
      const allOk = updated.every(c => c.status === 'ok')
      const criticalOk = updated.filter(c => ['comfyui', 'ffmpeg', 'disk_space'].includes(c.key)).every(c => c.status === 'ok')
      setOverall(allOk ? 'ready' : criticalOk ? 'checking' : 'blocked')
    } catch {
      setChecks(items.map(c => ({ ...c, status: 'error' as const, detail: '后端未启动，请先运行 python backend/main.py' })))
      setOverall('blocked')
    }
  }

  if (!show) return null

  const finish = () => {
    localStorage.setItem('avs-setup-done', '1')
    setShow(false)
    onDone()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.6)' }}>
      <div className="w-[560px] max-h-[85vh] overflow-auto p-8 rounded-2xl glass-strong"
        style={{ borderRadius: 'var(--theme-radius-lg)' }}>

        <h2 className="text-2xl font-bold mb-2" style={{ color: 'var(--theme-text)' }}>
          欢迎使用 AI Video Studio
        </h2>
        <p className="text-sm mb-6" style={{ color: 'var(--theme-text-secondary)' }}>
          首次使用前，一起检查运行环境。几分钟就好。
        </p>

        <div className="space-y-2 mb-6">
          {checks.map(c => (
            <div key={c.key} className="flex items-center gap-3 px-4 py-3 rounded-lg"
              style={{ background: 'var(--theme-bg)', borderRadius: 'var(--theme-radius-md)' }}>
              {c.status === 'checking' || c.status === 'pending' ? (
                <Loader2 size={18} className="animate-spin" style={{ color: 'var(--theme-text-secondary)' }} />
              ) : c.status === 'ok' ? (
                <Check size={18} style={{ color: 'var(--theme-success)' }} />
              ) : (
                <X size={18} style={{ color: 'var(--theme-danger)' }} />
              )}
              <span className="flex-1 text-sm font-medium" style={{ color: 'var(--theme-text)' }}>{c.label}</span>
              <span className="text-xs" style={{ color: c.status === 'error' ? 'var(--theme-danger)' : 'var(--theme-text-secondary)' }}>
                {c.detail}
              </span>
              {c.action && (
                <a href={c.action.url} target="_blank" rel="noopener noreferrer"
                  className="flex items-center gap-1 text-xs font-medium ml-2" style={{ color: 'var(--theme-accent)' }}>
                  <ExternalLink size={12} /> {c.action.label}
                </a>
              )}
            </div>
          ))}
        </div>

        {overall === 'ready' && (
          <div className="p-4 rounded-lg mb-4" style={{ background: 'var(--theme-success)', color: '#fff', borderRadius: 'var(--theme-radius-md)' }}>
            <div className="font-medium">所有检查通过，环境就绪</div>
            <div className="text-xs mt-1 opacity-80">ComfyUI 正常运行，模型文件齐全，可以开始创作了。</div>
          </div>
        )}

        {overall === 'blocked' && (
          <div className="p-4 rounded-lg mb-4" style={{ background: 'var(--theme-danger)', color: '#fff', borderRadius: 'var(--theme-radius-md)' }}>
            <div className="font-medium">存在需要解决的问题</div>
            <div className="text-xs mt-1 opacity-80">请先完成标记为红色的项目。ComfyUI 和 FFmpeg 必须安装，模型可在设置中下载。</div>
          </div>
        )}

        <div className="flex gap-3">
          <button onClick={runChecks}
            className="flex-1 py-2.5 rounded-lg text-sm font-medium"
            style={{ background: 'transparent', color: 'var(--theme-text)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
            重新检查
          </button>
          <button onClick={finish}
            className="flex-1 py-2.5 rounded-lg text-sm font-medium text-white"
            style={{ background: overall === 'ready' ? 'var(--theme-success)' : 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>
            {overall === 'ready' ? '进入应用' : '跳过检查，进入应用'}
          </button>
        </div>
      </div>
    </div>
  )
}
