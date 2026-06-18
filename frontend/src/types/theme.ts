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

export interface ThemeConfig {
  name: string
  colors: ThemeColors
  radii: ThemeRadii
}

export type ThemePreset = 'light' | 'dark' | 'mocha' | 'sakura' | 'synthwave' | 'tokyo-night' | 'custom'
