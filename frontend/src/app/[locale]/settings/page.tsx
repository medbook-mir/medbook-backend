'use client'

import { useRouter } from '@/i18n/navigation'
import { useEffect } from 'react'

const Settings = () => {
  const router = useRouter()

  useEffect(() => {
    router.replace('/settings/my-data')
  }, [router])

  return null
}

export default Settings
