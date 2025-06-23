'use client'

import { MainLogoWhite } from '@/assets/icons/MainLogoWhite'
import Link from 'next/link'
import { LangSelect } from '../shared/lang-select'

export default function Navbar() {
  return (
    <header className="mb-[67px] text-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <MainLogoWhite />

        <nav className="hidden gap-[60px] text-[18px] font-medium text-white md:flex">
          <Link href="#">
            <p className="text-white">How it works</p>
          </Link>
          <Link href="#">
            <p className="text-white">Medicals</p>
          </Link>
          <Link href="#">
            <p className="text-white">Blogs</p>
          </Link>
          <Link href="#">
            <p className="text-white">Healthy training</p>
          </Link>
        </nav>

        <div className="flex items-center gap-4">
          <LangSelect />
          <button className="rounded-full border border-white px-[16px] py-[11px] text-[14px] transition hover:bg-white hover:text-teal-800">
            For doctors
          </button>
          <button className="rounded-full bg-white px-[16px] py-[11px] text-sm font-semibold text-teal-800 transition hover:bg-gray-200">
            Login
          </button>
        </div>
      </div>
    </header>
  )
}
