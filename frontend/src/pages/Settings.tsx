import { useState } from 'react'
import { useThemeCtx } from '../hooks/useThemeCtx'
import { PRESETS } from '../lib/themes'
import type { ThemePreset, ThemeConfig } from '../types/theme'

const PRESET_ORDER: ThemePreset[] = ['light', 'dark', 'mocha', 'sakura', 'synthwave', 'tokyo-night']

const COLOR_KEYS: (keyof ThemeConfig['colors'])[] = ['bg', 'surface', 'border', 'text', 'textSecondary', 'accent', 'accentHover', 'danger', 'success']
const RADIUS_KEYS: (keyof ThemeConfig['radii'])[] = ['sm', 'md', 'lg']

export default function Settings() {
  const { preset, config, switchPreset, updateCustom, exportTheme, importTheme } = useThemeCtx()
  const [activeTab, setActiveTab] = useState<'theme' | 'api' | 'system'>('theme')
  const [apiKeys, setApiKeys] = useState({
    deepseek: '',
    bailian: '',
  })

  return (
    <div className="max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-6" style={{ color: 'var(--theme-text)' }}>设置</h1>

      <div className="flex gap-1 mb-6 p-1 rounded-lg" style={{ background: 'var(--theme-bg)' }}>
        {(['theme', 'api', 'system'] as const).map((t) => (
          <button
            key={t}
            onClick={() => setActiveTab(t)}
            className="flex-1 py-2 text-sm font-medium rounded-md transition-colors"
            style={{
              background: activeTab === t ? 'var(--theme-surface)' : 'transparent',
              color: activeTab === t ? 'var(--theme-text)' : 'var(--theme-text-secondary)',
            }}
          >
            {{ theme: '主题', api: 'API Key', system: '系统' }[t]}
          </button>
        ))}
      </div>

      {activeTab === 'theme' && (
        <div className="space-y-6">
          <div>
            <h3 className="text-sm font-medium mb-3" style={{ color: 'var(--theme-text)' }}>
              预设主题
            </h3>
            <div className="grid grid-cols-3 gap-2">
              {PRESET_ORDER.map((key) => {
                const t = PRESETS[key]
                return (
                  <button
                    key={key}
                    onClick={() => switchPreset(key)}
                    className="p-3 rounded-lg text-left text-sm transition-all"
                    style={{
                      background: t.colors.surface,
                      border: `2px solid ${preset === key ? t.colors.accent : t.colors.border}`,
                      borderRadius: 'var(--theme-radius-md)',
                    }}
                  >
                    <div className="flex gap-1 mb-1.5">
                      {[t.colors.accent, t.colors.bg, t.colors.text].map((c) => (
                        <div key={c} className="w-4 h-4 rounded-full" style={{ background: c }} />
                      ))}
                    </div>
                    <span style={{ color: t.colors.text }}>{t.name}</span>
                  </button>
                )
              })}
            </div>
          </div>

          {preset === 'custom' && (
            <>
              <div>
                <h3 className="text-sm font-medium mb-3" style={{ color: 'var(--theme-text)' }}>
                  颜色
                </h3>
                <div className="grid grid-cols-3 gap-3">
                  {COLOR_KEYS.map((k) => (
                    <label key={k} className="flex items-center gap-2 text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
                      <input
                        type="color"
                        value={config.colors[k]}
                        onChange={(e) => updateCustom({ ...config, colors: { ...config.colors, [k]: e.target.value } })}
                        className="w-8 h-8 rounded cursor-pointer border-0"
                      />
                      {k}
                    </label>
                  ))}
                </div>
              </div>
              <div>
                <h3 className="text-sm font-medium mb-3 mt-4" style={{ color: 'var(--theme-text)' }}>
                  模糊强度
                </h3>
                {(['sidebar','card','modal','panel','background'] as const).map(k => (
                  <label key={k} className="flex items-center gap-2 text-sm mb-2" style={{ color: 'var(--theme-text-secondary)' }}>
                    <span className="w-16">{{sidebar:'侧栏',card:'卡片',modal:'弹窗',panel:'面板',background:'背景'}[k]}</span>
                    <input type="range" min="0" max="32" value={parseInt(config.blur[k])} onChange={e => updateCustom({...config, blur:{...config.blur, [k]:`${e.target.value}px`}})}
                      className="flex-1" />
                    <span className="w-8 text-xs">{config.blur[k]}</span>
                  </label>
                ))}
                <h3 className="text-sm font-medium mb-3 mt-4" style={{ color: 'var(--theme-text)' }}>
                  圆角
                </h3>
                <div className="flex gap-4">
                  {RADIUS_KEYS.map((k) => (
                    <label key={k} className="flex items-center gap-2 text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
                      {k}
                      <input
                        type="text"
                        value={config.radii[k]}
                        onChange={(e) => updateCustom({ ...config, radii: { ...config.radii, [k]: e.target.value } })}
                        className="w-20 px-2 py-1 rounded text-sm"
                        style={{
                          background: 'var(--theme-bg)',
                          color: 'var(--theme-text)',
                          border: '1px solid var(--theme-border)',
                          borderRadius: 'var(--theme-radius-sm)',
                        }}
                      />
                    </label>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Blur controls — available for ALL themes */}
          <div>
            <h3 className="text-sm font-medium mb-3" style={{ color: 'var(--theme-text)' }}>模糊强度</h3>
            {(['sidebar','card','modal','panel','background'] as const).map(k => (
              <label key={k} className="flex items-center gap-2 text-sm mb-2" style={{ color: 'var(--theme-text-secondary)' }}>
                <span className="w-16">{{sidebar:'侧栏',card:'卡片',modal:'弹窗',panel:'面板',background:'背景'}[k]}</span>
                <input type="range" min="0" max="32" value={parseInt(config.blur?.[k] || '0')} onChange={e => updateCustom({...config, blur:{...config.blur, [k]:`${e.target.value}px`}})}
                  className="flex-1" />
                <span className="w-8 text-xs">{config.blur?.[k] || '0px'}</span>
              </label>
            ))}
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => {
                const json = exportTheme()
                const blob = new Blob([json], { type: 'application/json' })
                const url = URL.createObjectURL(blob)
                const a = document.createElement('a')
                a.href = url; a.download = 'theme.json'; a.click()
                URL.revokeObjectURL(url)
              }}
              className="px-4 py-2 rounded-lg text-sm font-medium"
              style={{
                background: 'transparent',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              导出主题
            </button>
            <label
              className="px-4 py-2 rounded-lg text-sm font-medium cursor-pointer"
              style={{
                background: 'var(--theme-accent)',
                color: '#fff',
                borderRadius: 'var(--theme-radius-md)',
              }}
            >
              导入主题
              <input
                type="file"
                accept=".json"
                className="hidden"
                onChange={(e) => {
                  const f = e.target.files?.[0]
                  if (!f) return
                  const reader = new FileReader()
                  reader.onload = () => importTheme(reader.result as string)
                  reader.readAsText(f)
                }}
              />
            </label>
          </div>
        </div>
      )}

      {activeTab === 'api' && (
        <div className="space-y-4">
          <label className="block" style={{ color: 'var(--theme-text)' }}>
            <span className="text-sm font-medium">DeepSeek API Key</span>
            <input
              type="text"
              value={apiKeys.deepseek}
              onChange={(e) => setApiKeys({ ...apiKeys, deepseek: e.target.value })}
              placeholder="sk-..."
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            />
          </label>
          <label className="block" style={{ color: 'var(--theme-text)' }}>
            <span className="text-sm font-medium">阿里云百炼 API Key</span>
            <input
              type="text"
              value={apiKeys.bailian}
              onChange={(e) => setApiKeys({ ...apiKeys, bailian: e.target.value })}
              placeholder="sk-..."
              className="w-full mt-1 px-3 py-2 rounded-lg text-sm"
              style={{
                background: 'var(--theme-bg)',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-md)',
              }}
            />
          </label>
          <button
            className="px-4 py-2 rounded-lg text-sm font-medium text-white"
            style={{
              background: 'var(--theme-accent)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            保存
          </button>
        </div>
      )}

      {activeTab === 'system' && (
        <div className="space-y-4 text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
          <div className="p-4 rounded-lg" style={{ background: 'var(--theme-surface)', borderRadius: 'var(--theme-radius-md)' }}>
            <p>ComfyUI 地址: http://127.0.0.1:8188</p>
            <p>模型路径: F:/ComfyUI/models/</p>
            <p>WAN 模型: N:/ComfyUI-WAN-models/</p>
          </div>
          <p>启动时自动检测环境，缺失项会在此显示。</p>
        </div>
      )}
    </div>
  )
}
