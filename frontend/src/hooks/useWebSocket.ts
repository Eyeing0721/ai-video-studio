import { useState, useRef, useEffect, useCallback } from 'react'

interface UseWebSocketOptions {
  taskId: string
  onMessage: (data: Record<string, unknown>) => void
}

interface UseWebSocketReturn {
  connected: boolean
  send: (data: Record<string, unknown>) => void
  close: () => void
}

export default function useWebSocket({ taskId, onMessage }: UseWebSocketOptions): UseWebSocketReturn {
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const retryCountRef = useRef(0)
  const retryTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const closedByUserRef = useRef(false)
  const onMessageRef = useRef(onMessage)
  onMessageRef.current = onMessage

  const clearRetryTimer = () => {
    if (retryTimerRef.current !== null) {
      clearTimeout(retryTimerRef.current)
      retryTimerRef.current = null
    }
  }

  const connect = useCallback(() => {
    if (closedByUserRef.current) return
    if (wsRef.current?.readyState === WebSocket.OPEN || wsRef.current?.readyState === WebSocket.CONNECTING) return

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/tasks/${taskId}`)
    wsRef.current = ws

    ws.onopen = () => {
      setConnected(true)
      retryCountRef.current = 0
    }

    ws.onmessage = (e: MessageEvent) => {
      try {
        const data = JSON.parse(e.data)
        onMessageRef.current(data)
      } catch {
        // ignore malformed messages
      }
    }

    ws.onclose = () => {
      setConnected(false)
      wsRef.current = null
      if (closedByUserRef.current) return

      // Exponential backoff: 1s, 2s, 4s, 8s, ... max 30s
      const delay = Math.min(1000 * Math.pow(2, retryCountRef.current), 30000)
      retryCountRef.current += 1
      retryTimerRef.current = setTimeout(() => {
        connect()
      }, delay)
    }

    ws.onerror = () => {
      // onclose will fire after onerror, reconnection handled there
    }
  }, [taskId])

  useEffect(() => {
    closedByUserRef.current = false
    retryCountRef.current = 0
    connect()

    return () => {
      closedByUserRef.current = true
      clearRetryTimer()
      if (wsRef.current) {
        wsRef.current.close()
        wsRef.current = null
      }
    }
  }, [connect])

  const send = useCallback((data: Record<string, unknown>) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data))
    }
  }, [])

  const close = useCallback(() => {
    closedByUserRef.current = true
    clearRetryTimer()
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }
    setConnected(false)
  }, [])

  return { connected, send, close }
}
