export interface ThemeColors {
  bg: string
  surface: string
  border: string
  text: string
  textSecondary: string
  accent: string
  accentHover: string
  danger: string
  success: string
}

export interface ThemeRadii {
  sm: string
  md: string
  lg: string
}

export interface ThemeBlur {
  sidebar: string
  card: string
  modal: string
  panel: string
}

export interface ThemeConfig {
  name: string
  colors: ThemeColors
  radii: ThemeRadii
  blur: ThemeBlur
  wallpaper: string
}

export type ThemePreset = 'light' | 'dark' | 'mocha' | 'sakura' | 'synthwave' | 'tokyo-night' | 'custom'
