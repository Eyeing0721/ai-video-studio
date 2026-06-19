export default function Spinner({ size = 20 }: { size?: number }) {
  return (
    <svg
      className="animate-spin"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
    >
      <path d="M21 12a9 9 0 1 1-6.219-8.56" opacity="0.25" />
      <path d="M21 12a9 9 0 1 1-6.219-8.56" opacity="0.75" strokeDasharray="60" strokeDashoffset="20" />
    </svg>
  )
}

export function PageSpinner({ label = '加载中...' }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center h-64 gap-4">
      <Spinner size={32} />
      <span className="text-sm" style={{ color: 'var(--theme-text-secondary)' }}>{label}</span>
    </div>
  )
}
