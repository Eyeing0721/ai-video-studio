import { useState, useEffect } from 'react'
import { useThemeCtx } from '../App'
import { PRESETS } from '../lib/themes'
import type { ThemePreset } from '../types/theme'

const PRESET_ORDER: ThemePreset[] = ['light', 'dark', 'mocha', 'sakura', 'synthwave', 'tokyo-night']

export default function ThemeWizard() {
  const { switchPreset } = useThemeCtx()
  const [show, setShow] = useState(false)
  const [step, setStep] = useState(0)

  useEffect(() => {
    const seen = localStorage.getItem('ai-video-studio-wizard-done')
    if (!seen) setShow(true)
  }, [])

  if (!show) return null

  const finish = () => {
    localStorage.setItem('ai-video-studio-wizard-done', '1')
    setShow(false)
  }

  const skip = () => {
    localStorage.setItem('ai-video-studio-wizard-done', '1')
    setShow(false)
  }

  if (step === 0) {
    return (
      <div
        className="fixed inset-0 z-50 flex items-center justify-center"
        style={{ background: 'rgba(0,0,0,0.5)' }}
      >
        <div
          className="w-[480px] p-8 rounded-2xl shadow-2xl"
          style={{
            background: 'var(--theme-surface)',
            borderRadius: 'var(--theme-radius-lg)',
          }}
        >
          <h2 className="text-2xl font-semibold mb-2" style={{ color: 'var(--theme-text)' }}>
            欢迎使用 AI Video Studio
          </h2>
          <p className="mb-6" style={{ color: 'var(--theme-text-secondary)' }}>
            在开始之前，选择一个你喜欢的主题风格。之后随时可以在设置中更改。
          </p>
          <div className="grid grid-cols-3 gap-3 mb-6">
            {PRESET_ORDER.map((key) => {
              const t = PRESETS[key]
              return (
                <button
                  key={key}
                  onClick={() => {
                    switchPreset(key)
                    setStep(1)
                  }}
                  className="p-3 rounded-lg text-sm font-medium transition-all hover:scale-105"
                  style={{
                    background: t.colors.surface,
                    color: t.colors.text,
                    border: `2px solid ${t.colors.border}`,
                    borderRadius: 'var(--theme-radius-md)',
                  }}
                >
                  <div className="flex gap-1 mb-2">
                    {[t.colors.accent, t.colors.bg, t.colors.text].map((c) => (
                      <div key={c} className="w-5 h-5 rounded-full" style={{ background: c }} />
                    ))}
                  </div>
                  {t.name}
                </button>
              )
            })}
          </div>
          <button
            onClick={skip}
            className="w-full py-2.5 rounded-lg text-sm font-medium"
            style={{
              background: 'transparent',
              color: 'var(--theme-text-secondary)',
              border: `1px solid var(--theme-border)`,
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            跳过，使用默认主题
          </button>
        </div>
      </div>
    )
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
      style={{ background: 'rgba(0,0,0,0.5)' }}
    >
      <div
        className="w-[480px] p-8 rounded-2xl shadow-2xl"
        style={{
          background: 'var(--theme-surface)',
          borderRadius: 'var(--theme-radius-lg)',
        }}
      >
        <h2 className="text-2xl font-semibold mb-4" style={{ color: 'var(--theme-text)' }}>
          主题预览
        </h2>
        <div
          className="p-6 rounded-lg mb-6 space-y-2"
          style={{
            background: 'var(--theme-bg)',
            borderRadius: 'var(--theme-radius-md)',
          }}
        >
          <div className="text-sm font-medium" style={{ color: 'var(--theme-text)' }}>
            标题文本示例
          </div>
          <div className="text-sm" style={{ color: 'var(--theme-text-secondary)' }}>
            这是正文文本的示例，展示可读性和对比度。
          </div>
          <div className="flex gap-2 pt-2">
            <div
              className="px-4 py-1.5 rounded-lg text-sm text-white font-medium"
              style={{
                background: 'var(--theme-accent)',
                borderRadius: 'var(--theme-radius-sm)',
              }}
            >
              主要按钮
            </div>
            <div
              className="px-4 py-1.5 rounded-lg text-sm font-medium"
              style={{
                background: 'transparent',
                color: 'var(--theme-text)',
                border: '1px solid var(--theme-border)',
                borderRadius: 'var(--theme-radius-sm)',
              }}
            >
              次要按钮
            </div>
          </div>
        </div>
        <div className="flex gap-3">
          <button
            onClick={() => setStep(0)}
            className="flex-1 py-2.5 rounded-lg text-sm font-medium"
            style={{
              background: 'transparent',
              color: 'var(--theme-text)',
              border: '1px solid var(--theme-border)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            返回选择
          </button>
          <button
            onClick={finish}
            className="flex-1 py-2.5 rounded-lg text-sm font-medium text-white"
            style={{
              background: 'var(--theme-accent)',
              borderRadius: 'var(--theme-radius-md)',
            }}
          >
            确认，开始使用
          </button>
        </div>
      </div>
    </div>
  )
}
