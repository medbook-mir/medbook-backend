'use client'

import { usePathname } from '@/i18n/navigation'

const ProtectedComponent = ({ children }: { children: React.ReactNode }) => {
  const pathname = usePathname()

  const authPaths = ['/login', '/register', '/forgot-password']

  const isAuthPage = authPaths.some((path) => pathname.includes(path))

  if (isAuthPage) {
    return null
  }

  return <>{children}</>
}

export default ProtectedComponent
