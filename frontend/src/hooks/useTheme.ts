import { useState, useEffect, useCallback } from 'react'
import type { ThemeConfig, ThemePreset } from '../types/theme'
import { PRESETS, applyTheme } from '../lib/themes'

const STORAGE_KEY = 'ai-video-studio-theme'

function getInitialPreset(): ThemePreset {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) return JSON.parse(saved).preset || 'light'
  } catch { /* ignore */ }
  return 'light'
}
function getInitialConfig(): ThemeConfig {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const parsed = JSON.parse(saved)
      if (parsed.preset === 'custom' && parsed.config) return parsed.config
      if (PRESETS[parsed.preset as ThemePreset]) return PRESETS[parsed.preset as ThemePreset]
    }
  } catch { /* ignore */ }
  return PRESETS.light
}
// Apply theme immediately before first render
const _initConfig = getInitialConfig()
applyTheme(_initConfig)

export function useTheme() {
  const [preset, setPreset] = useState<ThemePreset>(getInitialPreset)
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        return parsed.preset || 'light'
      } catch { /* ignore */ }
    }
    return 'light'
  })

  const [config, setConfig] = useState<ThemeConfig>(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        if (parsed.preset === 'custom' && parsed.config) return parsed.config
        if (PRESETS[parsed.preset as ThemePreset]) return PRESETS[parsed.preset as ThemePreset]
      } catch { /* ignore */ }
    }
    return PRESETS.light
  })

  useEffect(() => {
    applyTheme(config)
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ preset, config }))
  }, [config, preset])

  const switchPreset = useCallback((p: ThemePreset) => {
    setPreset(p)
    if (p !== 'custom') setConfig(PRESETS[p])
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ preset: p, config: PRESETS[p] }))
  }, [])

  const updateCustom = useCallback((c: ThemeConfig) => {
    setPreset('custom')
    setConfig(c)
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ preset: 'custom', config: c }))
  }, [])

  const exportTheme = useCallback(() => {
    return JSON.stringify({ preset, config }, null, 2)
  }, [preset, config])

  const importTheme = useCallback((json: string) => {
    const data = JSON.parse(json)
    if (data.config) {
      setConfig(data.config)
      setPreset(data.preset || 'custom')
    }
  }, [])

  return { preset, config, switchPreset, updateCustom, exportTheme, importTheme }
}
