'use client'

import { usePathname } from '@/i18n/navigation'

const ProtectedComponent = ({ children, paths }: { children: React.ReactNode; paths?: string[] }) => {
  const pathname = usePathname()

  const protectedPaths = [...(paths || []), '/login', '/register', '/forgot-password']

  const isProtectedPage = protectedPaths.some((path) => pathname.includes(path))

  if (isProtectedPage) {
    return null
  }

  return <>{children}</>
}

export default ProtectedComponent
