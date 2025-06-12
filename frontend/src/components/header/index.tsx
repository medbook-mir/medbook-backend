"use client";

import { MainLogoWhite } from "@/assets/icons/MainLogoWhite";
import Link from "next/link";
import { LangSelect } from "../shared/lang-select";

export default function Navbar() {
  return (
    <header className=" text-white mb-[67px]">
      <div className="max-w-7xl mx-auto flex justify-between items-center">
        <MainLogoWhite />

        <nav className="hidden md:flex gap-[60px] text-white text-[18px] font-medium">
          <Link href="#">How it works</Link>
          <Link href="#">Medicals</Link>
          <Link href="#">Blogs</Link>
          <Link href="#">Healthy training</Link>
        </nav>

        <div className="flex gap-4 items-center">
          <LangSelect />
          <button className="border border-white rounded-full px-[16px] py-[11px] text-[14px] hover:bg-white hover:text-teal-800 transition">
            For doctors
          </button>
          <button className="bg-white text-teal-800 font-semibold rounded-full px-[16px] py-[11px] text-sm hover:bg-gray-200 transition">
            Login
          </button>
        </div>
      </div>
    </header>
  );
}
