import type { ReactNode } from 'react'

interface Props {
  icon?: ReactNode
  title: string
  description?: string
  action?: ReactNode
}

export default function EmptyState({ icon, title, description, action }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-3">
      {icon && (
        <div className="mb-2 opacity-40" style={{ color: 'var(--theme-text-secondary)' }}>
          {icon}
        </div>
      )}
      <p className="text-base font-medium" style={{ color: 'var(--theme-text)' }}>{title}</p>
      {description && (
        <p className="text-sm max-w-sm text-center" style={{ color: 'var(--theme-text-secondary)' }}>
          {description}
        </p>
      )}
      {action && <div className="mt-2">{action}</div>}
    </div>
  )
}
