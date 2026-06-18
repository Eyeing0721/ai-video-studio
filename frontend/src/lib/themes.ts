import type { ThemeConfig, ThemePreset } from '../types/theme'

export const PRESETS: Record<ThemePreset, ThemeConfig> = {
  light: {
    name: '浅色模式',
    colors: {
      bg: '#F4F3F0',
      surface: '#FFFFFF',
      border: '#E5E0DA',
      text: '#2C2416',
      textSecondary: '#8C8378',
      accent: '#A47864',
      accentHover: '#8B6552',
      danger: '#D14343',
      success: '#4A9E6B',
    },
    radii: { sm: '4px', md: '8px', lg: '14px' },
  },
  dark: {
    name: '深色模式',
    colors: {
      bg: '#1A1B1E',
      surface: '#252629',
      border: '#383A3F',
      text: '#E8E6E3',
      textSecondary: '#9A9896',
      accent: '#C0997A',
      accentHover: '#A88764',
      danger: '#E85D5D',
      success: '#5BBF7B',
    },
    radii: { sm: '4px', md: '8px', lg: '14px' },
  },
  mocha: {
    name: '潘通 摩卡慕斯',
    colors: {
      bg: '#F5EFE8',
      surface: '#FDFAF6',
      border: '#D4C4B0',
      text: '#3E2E20',
      textSecondary: '#8C7865',
      accent: '#A47864',
      accentHover: '#8B6552',
      danger: '#C45C4A',
      success: '#5A8F6E',
    },
    radii: { sm: '4px', md: '10px', lg: '16px' },
  },
  sakura: {
    name: '和风樱花',
    colors: {
      bg: '#FDF6F5',
      surface: '#FFFFFF',
      border: '#FEDFE1',
      text: '#4A3346',
      textSecondary: '#9B8398',
      accent: '#D4A5B9',
      accentHover: '#C08FA6',
      danger: '#C4627A',
      success: '#68BE8D',
    },
    radii: { sm: '6px', md: '12px', lg: '20px' },
  },
  synthwave: {
    name: '合成波',
    colors: {
      bg: '#120020',
      surface: '#1E0038',
      border: '#3D0070',
      text: '#F0E8FF',
      textSecondary: '#B8A0D8',
      accent: '#FF6B9D',
      accentHover: '#E85585',
      danger: '#FF4470',
      success: '#00FFAA',
    },
    radii: { sm: '2px', md: '6px', lg: '12px' },
  },
  'tokyo-night': {
    name: '东京之夜',
    colors: {
      bg: '#0F111B',
      surface: '#1A1D2E',
      border: '#2A2E42',
      text: '#D4D7E5',
      textSecondary: '#8088A0',
      accent: '#7B9AEA',
      accentHover: '#6380D0',
      danger: '#E8566A',
      success: '#50C878',
    },
    radii: { sm: '4px', md: '8px', lg: '14px' },
  },
  custom: {
    name: '自定义',
    colors: {
      bg: '#F4F3F0',
      surface: '#FFFFFF',
      border: '#E5E0DA',
      text: '#2C2416',
      textSecondary: '#8C8378',
      accent: '#A47864',
      accentHover: '#8B6552',
      danger: '#D14343',
      success: '#4A9E6B',
    },
    radii: { sm: '4px', md: '8px', lg: '14px' },
  },
}

export function applyTheme(config: ThemeConfig) {
  const root = document.documentElement
  root.style.setProperty('--theme-bg', config.colors.bg)
  root.style.setProperty('--theme-surface', config.colors.surface)
  root.style.setProperty('--theme-border', config.colors.border)
  root.style.setProperty('--theme-text', config.colors.text)
  root.style.setProperty('--theme-text-secondary', config.colors.textSecondary)
  root.style.setProperty('--theme-accent', config.colors.accent)
  root.style.setProperty('--theme-accent-hover', config.colors.accentHover)
  root.style.setProperty('--theme-danger', config.colors.danger)
  root.style.setProperty('--theme-success', config.colors.success)
  root.style.setProperty('--theme-radius-sm', config.radii.sm)
  root.style.setProperty('--theme-radius-md', config.radii.md)
  root.style.setProperty('--theme-radius-lg', config.radii.lg)

  const isDark = ['dark', 'synthwave', 'tokyo-night'].some(n => config.name === PRESETS[n as ThemePreset]?.name)
  const cs = isDark ? 'dark' : 'light'
  document.documentElement.style.colorScheme = cs
}
