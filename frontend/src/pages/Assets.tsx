import { useState, useEffect, useRef } from 'react'
import { Play, Pause, Eye, X } from 'lucide-react'

const API = 'http://127.0.0.1:8000'

type AssetType = '全部' | 'BGM' | 'LUT' | 'SFX'
const TYPES: AssetType[] = ['全部', 'BGM', 'LUT', 'SFX']

interface BgmItem { id: string; name: string; genre: string; tags: string[]; mood: string[]; duration_sec: number; bpm: number; url: string; license: string }
interface LutItem { id: string; name: string; name_cn: string; style: string; tags: string[]; use_case: string[]; url: string }
interface SfxItem { id: string; name: string; name_cn: string; type: string; tags: string[]; use_case: string[] }

const SAMPLE_IMAGE = 'data:image/svg+xml,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="400" height="280">' +
  '<defs>' +
    '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#4A90D9"/><stop offset="60%" stop-color="#87CEEB"/><stop offset="100%" stop-color="#B8D4E8"/></linearGradient>' +
    '<linearGradient id="mtn" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#5D7B5E"/><stop offset="100%" stop-color="#3D5A3E"/></linearGradient>' +
    '<linearGradient id="grass" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#7BA669"/><stop offset="100%" stop-color="#5C8A4A"/></linearGradient>' +
    '<radialGradient id="sun" cx="0.75" cy="0.25" r="0.15"><stop offset="0%" stop-color="#FFF9E0"/><stop offset="100%" stop-color="#FFD700"/></radialGradient>' +
  '</defs>' +
  '<rect width="400" height="180" fill="url(#sky)"/>' +
  '<circle cx="300" cy="40" r="45" fill="#FFF9E0" opacity="0.9"/>' +
  '<polygon points="80,180 200,60 320,180" fill="url(#mtn)"/>' +
  '<polygon points="150,180 280,80 400,180" fill="#4A6B4A" opacity="0.7"/>' +
  '<rect x="0" y="165" width="400" height="115" fill="url(#grass)"/>' +
  '<rect x="0" y="165" width="400" height="3" fill="#3D5A3E" opacity="0.5"/>' +
  '<circle cx="120" cy="240" r="25" fill="#E8A87C"/>' +
  '<circle cx="125" cy="225" r="12" fill="#D4956C"/>' +
  '<text x="160" y="245" fill="#5C3A2E" font-size="11" font-family="sans-serif" font-weight="bold">人物</text>' +
  '</svg>'
)

export default function Assets() {
  const [activeType, setActiveType] = useState<AssetType>('全部')
  const [bgms, setBgms] = useState<BgmItem[]>([])
  const [luts, setLuts] = useState<LutItem[]>([])
  const [sfxs, setSfxs] = useState<SfxItem[]>([])
  const [playing, setPlaying] = useState<string | null>(null)
  const [previewLut, setPreviewLut] = useState<LutItem | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  useEffect(() => {
    fetch(`${API}/api/bgm`).then(r => r.json()).then(d => Array.isArray(d) && setBgms(d.slice(0, 20))).catch(() => {})
    fetch(`${API}/api/luts`).then(r => r.json()).then(d => Array.isArray(d) && setLuts(d)).catch(() => {})
    fetch(`${API}/api/sfx`).then(r => r.json()).then(d => Array.isArray(d) && setSfxs(d)).catch(() => {})
  }, [])

  const togglePlay = (id: string, url?: string) => {
    if (playing === id) {
      audioRef.current?.pause()
      setPlaying(null)
      return
    }
    if (audioRef.current) {
      audioRef.current.pause()
      audioRef.current.src = url || ''
      audioRef.current.play().catch(() => {})
      setPlaying(id)
    }
  }

  const filtered = [
    ...(activeType === '全部' || activeType === 'BGM' ? bgms.map(b => ({ ...b, _type: 'BGM' as const })) : []),
    ...(activeType === '全部' || activeType === 'LUT' ? luts.map(l => ({ ...l, _type: 'LUT' as const })) : []),
    ...(activeType === '全部' || activeType === 'SFX' ? sfxs.map(s => ({ ...s, _type: 'SFX' as const })) : []),
  ]

  return (
    <div className="max-w-5xl mx-auto">
      <audio ref={audioRef} onEnded={() => setPlaying(null)} className="hidden" />

      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold" style={{ color: 'var(--theme-text)' }}>资产库</h1>
        <button className="px-4 py-2 rounded-lg text-sm font-medium text-white"
          style={{ background: 'var(--theme-accent)', borderRadius: 'var(--theme-radius-md)' }}>上传资产</button>
      </div>

      <div className="flex gap-2 mb-6">
        {TYPES.map(t => (
          <button key={t} onClick={() => setActiveType(t)}
            className="px-4 py-2 rounded-lg text-sm font-medium transition-all"
            style={{
              background: activeType === t ? 'var(--theme-accent)' : 'var(--theme-surface)',
              color: activeType === t ? '#fff' : 'var(--theme-text)',
              border: `1px solid ${activeType === t ? 'var(--theme-accent)' : 'var(--theme-border)'}`,
              borderRadius: 'var(--theme-radius-md)',
            }}>{t}</button>
        ))}
        <span className="ml-auto text-xs self-center" style={{ color: 'var(--theme-text-secondary)' }}>
          {filtered.length} 项
        </span>
      </div>

      <div className="grid grid-cols-2 gap-4">
        {filtered.map((item, i) => (
          <AssetCard
            key={`${item._type}-${i}`}
            item={item}
            isPlaying={playing === ('id' in item ? item.id : `item-${i}`)}
            onPlay={() => {
              const id = 'id' in item ? item.id : `item-${i}`
              const url = 'url' in item ? (item as BgmItem).url : undefined
              togglePlay(id, url)
            }}
            onPreview={() => item._type === 'LUT' && setPreviewLut(item as unknown as LutItem)}
          />
        ))}
      </div>

      {filtered.length === 0 && (
        <p className="text-center py-20 text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
          暂无资产。启动后端后自动加载。
        </p>
      )}

      {/* LUT Preview Modal */}
      {previewLut && (
        <div className="fixed inset-0 z-50 flex items-center justify-center" style={{ background: 'rgba(0,0,0,0.7)' }}
          onClick={() => setPreviewLut(null)}>
          <div className="glass-strong p-6 rounded-2xl max-w-lg w-full" onClick={e => e.stopPropagation()}
            style={{ borderRadius: 'var(--theme-radius-lg)' }}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold" style={{ color: 'var(--theme-text)' }}>{previewLut.name_cn || previewLut.name}</h3>
              <button onClick={() => setPreviewLut(null)}><X size={20} /></button>
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <div className="text-xs mb-1" style={{ color: 'var(--theme-text-secondary)' }}>原始</div>
                <img src={SAMPLE_IMAGE} alt="原始" className="w-full rounded-lg" style={{ borderRadius: 'var(--theme-radius-md)' }} />
              </div>
              <div>
                <div className="text-xs mb-1" style={{ color: 'var(--theme-text-secondary)' }}>{previewLut.name} 效果</div>
                <div className="relative w-full rounded-lg overflow-hidden" style={{ borderRadius: 'var(--theme-radius-md)' }}>
                  <img src={SAMPLE_IMAGE} alt="LUT效果" className="w-full"
                    style={{ filter: `contrast(1.2) saturate(1.1) hue-rotate(${previewLut.style === 'cinematic' ? '-10deg' : previewLut.style === 'vintage' ? '15deg' : previewLut.style === 'urban' ? '-25deg' : '0deg'})` }} />
                  <div className="absolute inset-0 flex items-center justify-center"
                    style={{ background: previewLut.style === 'cinematic' ? 'rgba(255,140,0,0.15)' : previewLut.style === 'vintage' ? 'rgba(180,130,80,0.2)' : previewLut.style === 'urban' ? 'rgba(0,150,255,0.12)' : previewLut.style === 'japanese' ? 'rgba(255,150,180,0.12)' : 'transparent' }} />
                </div>
              </div>
            </div>
            <div className="flex gap-1.5 flex-wrap mb-3">
              {previewLut.tags?.map(t => (
                <span key={t} className="text-xs px-2 py-0.5 rounded-full"
                  style={{ background: 'var(--theme-bg)', color: 'var(--theme-text-secondary)' }}>{t}</span>
              ))}
            </div>
            <p className="text-xs" style={{ color: 'var(--theme-text-secondary)' }}>
              适用: {previewLut.use_case?.join(' / ') || '通用'}
            </p>
          </div>
        </div>
      )}
    </div>
  )
}

function AssetCard({ item, isPlaying, onPlay, onPreview }: {
  item: Record<string, unknown> & { _type: string }
  isPlaying: boolean
  onPlay: () => void
  onPreview: () => void
}) {
  const t = item._type
  const name = (item.name_cn as string) || (item.name as string) || '未命名'
  const tags = (item.tags as string[]) || []
  const mood = (item.mood as string[]) || []

  return (
    <div className="p-4 rounded-lg transition-all hover:scale-[1.01]"
      style={{ background: 'var(--theme-surface)', border: '1px solid var(--theme-border)', borderRadius: 'var(--theme-radius-md)' }}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs px-2 py-0.5 rounded font-medium"
          style={{ background: 'var(--theme-bg)', color: 'var(--theme-accent)' }}>{t}</span>
        <div className="flex gap-2">
          {t === 'BGM' && (
            <>
              <span className="text-xs" style={{ color: 'var(--theme-text-secondary)' }}>
                {item.bpm ? `${item.bpm} BPM` : ''} {(item as BgmItem).duration_sec ? `${Math.round((item as BgmItem).duration_sec / 60)}:${String(Math.round((item as BgmItem).duration_sec % 60)).padStart(2, '0')}` : ''}
              </span>
              <button onClick={onPlay}
                className="w-7 h-7 rounded-full flex items-center justify-center transition-all"
                style={{ background: isPlaying ? 'var(--theme-accent)' : 'var(--theme-bg)', color: isPlaying ? '#fff' : 'var(--theme-text-secondary)' }}>
                {isPlaying ? <Pause size={14} /> : <Play size={14} />}
              </button>
            </>
          )}
          {t === 'SFX' && (
            <button onClick={onPlay}
              className="w-7 h-7 rounded-full flex items-center justify-center"
              style={{ background: isPlaying ? 'var(--theme-accent)' : 'var(--theme-bg)', color: isPlaying ? '#fff' : 'var(--theme-text-secondary)' }}>
              {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            </button>
          )}
          {t === 'LUT' && (
            <button onClick={onPreview}
              className="flex items-center gap-1 text-xs font-medium"
              style={{ color: 'var(--theme-accent)' }}>
              <Eye size={14} /> 预览效果
            </button>
          )}
        </div>
      </div>
      <div className="font-medium text-sm mb-2" style={{ color: 'var(--theme-text)' }}>{name}</div>
      <div className="flex gap-1.5 flex-wrap">
        {[...tags, ...mood].slice(0, 5).map((tag: string) => (
          <span key={tag} className="text-xs px-2 py-0.5 rounded-full"
            style={{ background: 'var(--theme-bg)', color: 'var(--theme-text-secondary)' }}>{tag}</span>
        ))}
      </div>
    </div>
  )
}
