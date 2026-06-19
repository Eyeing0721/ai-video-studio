import type { ThemeConfig, ThemePreset } from '../types/theme'

// SVG data URIs for wallpapers (compressed gradients that evoke each theme)
const WALLPAPERS = {
  light: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F3F0"/><stop offset="50%" stop-color="#EDE9E2"/><stop offset="100%" stop-color="#E5E0DA"/></linearGradient></defs><rect width="800" height="600" fill="url(#g)"/></svg>'),
  dark: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1A1B1E"/><stop offset="50%" stop-color="#202125"/><stop offset="100%" stop-color="#15161A"/></linearGradient></defs><rect width="800" height="600" fill="url(#g)"/></svg>'),
  mocha: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><radialGradient id="g" cx="0.3" cy="0.3" r="0.8"><stop offset="0" stop-color="#A47864" stop-opacity="0.15"/><stop offset="100%" stop-color="#F5EFE8"/></radialGradient></defs><rect width="800" height="600" fill="url(#g)"/></svg>'),
  sakura: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><radialGradient id="g1" cx="0.2" cy="0.3" r="0.6"><stop offset="0" stop-color="#FEDFE1" stop-opacity="0.3"/><stop offset="100%" stop-color="#FDF6F5"/></radialGradient><radialGradient id="g2" cx="0.8" cy="0.7" r="0.5"><stop offset="0" stop-color="#D4A5B9" stop-opacity="0.1"/><stop offset="100%" stop-color="#FDF6F5"/></radialGradient></defs><rect width="800" height="600" fill="url(#g1)"/><rect width="800" height="600" fill="url(#g2)"/></svg>'),
  synthwave: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0020"/><stop offset="60%" stop-color="#1A0033"/><stop offset="100%" stop-color="#FF6B9D" stop-opacity="0.3"/></linearGradient><linearGradient id="sun" x1="0" y1="1" x2="1" y2="0"><stop offset="0" stop-color="#FF6B9D"/><stop offset="40%" stop-color="#FF4470"/><stop offset="100%" stop-color="#FFD700"/></linearGradient></defs><rect width="800" height="600" fill="url(#sky)"/><circle cx="400" cy="480" r="200" fill="url(#sun)" opacity="0.6"/><line x1="0" y1="400" x2="800" y2="400" stroke="#FF6B9D" opacity="0.3" stroke-width="2"/><line x1="0" y1="420" x2="800" y2="420" stroke="#00FFFF" opacity="0.2" stroke-width="1"/><line x1="0" y1="440" x2="800" y2="440" stroke="#FF6B9D" opacity="0.2" stroke-width="1"/><line x1="0" y1="460" x2="800" y2="460" stroke="#00FFFF" opacity="0.15" stroke-width="1"/><line x1="0" y1="480" x2="800" y2="480" stroke="#FF6B9D" opacity="0.1" stroke-width="1"/></svg>'),
  tokyo: 'data:image/svg+xml,' + encodeURIComponent('<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0A0F25"/><stop offset="50%" stop-color="#161B35"/><stop offset="100%" stop-color="#1A1D2E"/></linearGradient><radialGradient id="neon1" cx="0.3" cy="0.5" r="0.3"><stop offset="0" stop-color="#F5A623" stop-opacity="0.15"/><stop offset="100%" stop-color="transparent"/></radialGradient><radialGradient id="neon2" cx="0.7" cy="0.4" r="0.35"><stop offset="0" stop-color="#7B9AEA" stop-opacity="0.12"/><stop offset="100%" stop-color="transparent"/></radialGradient></defs><rect width="800" height="600" fill="url(#sky)"/><rect width="800" height="600" fill="url(#neon1)"/><rect width="800" height="600" fill="url(#neon2)"/><circle cx="600" cy="150" r="3" fill="#F5A623" opacity="0.6"/><circle cx="200" cy="80" r="2" fill="#F5A623" opacity="0.4"/><circle cx="350" cy="120" r="2" fill="#7B9AEA" opacity="0.5"/></svg>'),
}

export const PRESETS: Record<ThemePreset, ThemeConfig> = {
  light: {
    name: '浅色模式',
    colors: { bg: '#F4F3F0', surface: '#FFFFFF', border: '#E5E0DA', text: '#2C2416', textSecondary: '#8C8378', accent: '#A47864', accentHover: '#8B6552', danger: '#D14343', success: '#4A9E6B' },
    radii: { sm: '4px', md: '8px', lg: '14px' },
    blur: { sidebar: '12px', card: '8px', modal: '20px', panel: '4px' },
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
    blur: { sidebar: '12px', card: '8px', modal: '20px', panel: '4px' },
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
  // Wallpaper
  root.style.setProperty('--wallpaper', `url(${config.wallpaper})`)
  root.style.backgroundImage = `url(${config.wallpaper})`
  root.style.backgroundSize = 'cover'
  root.style.backgroundAttachment = 'fixed'

  const isDark = ['dark', 'synthwave', 'tokyo-night'].includes(config.name)
  document.documentElement.style.colorScheme = isDark ? 'dark' : 'light'
}
