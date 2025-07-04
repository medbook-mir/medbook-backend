'use client'

import { Link, usePathname } from '@/i18n/navigation'
import { sidebarData } from './sidebar-data'

const Sidebar = () => {
  const pathname = usePathname()

  return (
    <aside className="flex flex-col rounded-2xl border-2 border-[#E9ECF4] pb-[30px] text-[16px] leading-1.5 font-normal">
      <div className="flex flex-col text-black">
        {sidebarData.map((item) => {
          const isActive = pathname.includes(item.href)
          return (
            <Link
              href={`/settings/${item.href}`}
              key={item.href}
              className={`px-8 py-6 ${isActive ? 'bg-[#F4F6FA] font-semibold text-black' : 'font-normal text-gray-500'}`}
            >
              {item.title}
            </Link>
          )
        })}
      </div>
      <button className="px-8 py-6 text-start text-[#FF4242]">Logout</button>
    </aside>
  )
}
export default Sidebar
