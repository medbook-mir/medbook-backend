'use client'

import { FilledButton } from '@/components/ui/filled-button'
import { useRouter } from '@/i18n/navigation'
import { startTransition } from 'react'

const ErrorBoundary = ({ error, reset }: { error: Error; reset: () => void }) => {
  const router = useRouter()
  const reload = () => {
    startTransition(() => {
      router.refresh()
      reset()
    })
  }

  return (
    <div className="flex items-center justify-center">
      <p>{error.message}</p>
      <FilledButton onClick={() => reload()}>Try again</FilledButton>
    </div>
  )
}

export default ErrorBoundary
