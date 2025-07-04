'use client'

import { MainLogoWhite } from '@/assets/icons/MainLogoWhite'
import { LangSelect } from '../shared/lang-select'
import { Link, usePathname, useRouter } from '@/i18n/navigation'
import { Container } from '@/theme/container'
import { useAppDispatch } from '@/redux/store'
import { homePageNavItems, otherPagesNavItems } from './data'
import { openModal } from '@/redux/reducers/modals'

export default function Navbar() {
  const pathname = usePathname()
  const router = useRouter()
  const dispatch = useAppDispatch()

  const isHomePage = pathname === '/'
  const navItems = isHomePage ? homePageNavItems : otherPagesNavItems

  const handleLogin = () => {
    if (pathname === '/') {
      router.push('/login')
    } else {
      dispatch(openModal('loginModal'))
    }
  }

  return (
    <header className="bg-[#046D5F] py-8 text-white">
      <Container>
        <div className="flex items-center justify-between">
          <Link href="/">
            <MainLogoWhite />
          </Link>

          <nav className="hidden gap-[60px] text-[18px] font-medium text-white md:flex">
            {navItems.map((item, index) => (
              <Link href={item.href} key={index}>
                <p className="text-white">{item.title}</p>
              </Link>
            ))}
          </nav>

          <div className="flex items-center gap-4">
            <LangSelect />
            <button className="h-[40px] rounded-full border border-white px-[16px] text-[14px] transition hover:bg-white hover:text-teal-800">
              For doctors
            </button>
            <button
              onClick={handleLogin}
              className="flex h-[40px] items-center rounded-full bg-white px-[16px] text-sm font-semibold text-teal-800 transition hover:bg-gray-200"
            >
              Login
            </button>
          </div>
        </div>
      </Container>
    </header>
  )
}
