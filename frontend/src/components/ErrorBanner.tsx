interface Props {
  message: string
  onRetry?: () => void
  onDismiss?: () => void
}

export default function ErrorBanner({ message, onRetry, onDismiss }: Props) {
  return (
    <div
      className="flex items-center gap-3 px-4 py-3 rounded-lg text-sm"
      style={{ background: 'var(--theme-danger)', color: '#fff', borderRadius: 'var(--theme-radius-md)' }}
    >
      <span className="flex-1">{message}</span>
      {onRetry && (
        <button onClick={onRetry} className="font-medium underline underline-offset-2">
          重试
        </button>
      )}
      {onDismiss && (
        <button onClick={onDismiss} className="opacity-70 hover:opacity-100">X</button>
      )}
    </div>
  )
}
