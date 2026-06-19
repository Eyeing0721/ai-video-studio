import type { ThemeConfig, ThemePreset } from '../types/theme'

// Theme wallpapers — real photos for scenic, CSS textures for minimal
const WALLPAPERS: Record<string, string> = {
  light: 'none',
  dark: 'none',
  mocha: 'none',
  sakura: 'url(/media/wallpapers/sakura.jpg)',
  synthwave: 'url(/media/wallpapers/synthwave.jpg)',
  tokyo: 'url(/media/wallpapers/tokyo.jpg)',
}

export const PRESETS: Record<ThemePreset, ThemeConfig> = {
  light: {
    name: '浅色模式',
    colors: { bg: '#F4F3F0', surface: '#FFFFFF', border: '#E5E0DA', text: '#2C2416', textSecondary: '#8C8378', accent: '#A47864', accentHover: '#8B6552', danger: '#D14343', success: '#4A9E6B' },
    radii: { sm: '4px', md: '8px', lg: '14px' },
    blur: { sidebar: '12px', card: '8px', modal: '20px', panel: '4px', background: '0px' },
    wallpaper: WALLPAPERS.light,
  },
  dark: {
    name: '深色模式',
    colors: { bg: '#1A1B1E', surface: '#252629', border: '#383A3F', text: '#E8E6E3', textSecondary: '#9A9896', accent: '#C0997A', accentHover: '#A88764', danger: '#E85D5D', success: '#5BBF7B' },
    radii: { sm: '4px', md: '8px', lg: '14px' },
    blur: { sidebar: '12px', card: '8px', modal: '20px', panel: '4px' },
    wallpaper: WALLPAPERS.dark,
  },
  mocha: {
    name: '潘通 摩卡慕斯',
    colors: { bg: '#F5EFE8', surface: '#FDFAF6', border: '#D4C4B0', text: '#3E2E20', textSecondary: '#8C7865', accent: '#A47864', accentHover: '#8B6552', danger: '#C45C4A', success: '#5A8F6E' },
    radii: { sm: '4px', md: '10px', lg: '16px' },
    blur: { sidebar: '16px', card: '10px', modal: '24px', panel: '6px' },
    wallpaper: WALLPAPERS.mocha,
  },
  sakura: {
    name: '和风樱花',
    colors: { bg: '#FDF6F5', surface: '#FFFFFF', border: '#FEDFE1', text: '#4A3346', textSecondary: '#9B8398', accent: '#D4A5B9', accentHover: '#C08FA6', danger: '#C4627A', success: '#68BE8D' },
    radii: { sm: '6px', md: '12px', lg: '20px' },
    blur: { sidebar: '18px', card: '12px', modal: '28px', panel: '8px' },
    wallpaper: WALLPAPERS.sakura,
  },
  synthwave: {
    name: '合成波',
    colors: { bg: '#120020', surface: '#1E0038', border: '#3D0070', text: '#F0E8FF', textSecondary: '#B8A0D8', accent: '#FF6B9D', accentHover: '#E85585', danger: '#FF4470', success: '#00FFAA' },
    radii: { sm: '2px', md: '6px', lg: '12px' },
    blur: { sidebar: '14px', card: '10px', modal: '24px', panel: '6px' },
    wallpaper: WALLPAPERS.synthwave,
  },
  'tokyo-night': {
    name: '东京之夜',
    colors: { bg: '#0F111B', surface: '#1A1D2E', border: '#2A2E42', text: '#D4D7E5', textSecondary: '#8088A0', accent: '#7B9AEA', accentHover: '#6380D0', danger: '#E8566A', success: '#50C878' },
    radii: { sm: '4px', md: '8px', lg: '14px' },
    blur: { sidebar: '16px', card: '10px', modal: '26px', panel: '6px' },
    wallpaper: WALLPAPERS.tokyo,
  },
  custom: {
    name: '自定义',
    colors: { bg: '#F4F3F0', surface: '#FFFFFF', border: '#E5E0DA', text: '#2C2416', textSecondary: '#8C8378', accent: '#A47864', accentHover: '#8B6552', danger: '#D14343', success: '#4A9E6B' },
    radii: { sm: '4px', md: '8px', lg: '14px' },
    blur: { sidebar: '12px', card: '8px', modal: '20px', panel: '4px', background: '0px' },
    wallpaper: WALLPAPERS.light,
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
  // Blur levels
  root.style.setProperty('--blur-sidebar', config.blur.sidebar)
  root.style.setProperty('--blur-card', config.blur.card)
  root.style.setProperty('--blur-modal', config.blur.modal)
  root.style.setProperty('--blur-panel', config.blur.panel)
  root.style.setProperty('--blur-background', config.blur.background)
  // Wallpaper
  document.body.style.backgroundImage = config.wallpaper
  document.body.style.backgroundSize = 'cover'
  document.body.style.backgroundAttachment = 'fixed'
  // Texture class for themes without photo wallpaper
  document.body.classList.remove('texture-light', 'texture-dark', 'texture-mocha')
  if (config.wallpaper === 'none') {
    if (config.name.includes('浅色') || config.name === 'light') document.body.classList.add('texture-light')
    else if (config.name.includes('深色') || config.name === 'dark') document.body.classList.add('texture-dark')
    else if (config.name.includes('摩卡')) document.body.classList.add('texture-mocha')
  }

  const isDark = ['dark', 'synthwave', 'tokyo-night'].includes(config.name)
  document.documentElement.style.colorScheme = isDark ? 'dark' : 'light'
}
