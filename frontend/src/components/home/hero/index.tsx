'use client'

import { images } from '@/assets'
import { LocationIcon } from '@/utils/icons/LocationIcon'
import { SearchIcon } from '@/utils/icons/SearchIcon'
import Image from 'next/image'
import { useState } from 'react'
import DoctorSearchResult from './search-result'

export default function HeroSection() {
  const [searchResult, setSearchResult] = useState('')
  return (
    <section className="text-white">
      <div className="mx-auto flex max-w-7xl flex-col-reverse items-center justify-between gap-10 lg:flex-row">
        <div className="relative">
          <h1 className="mb-6 w-[450px] text-[56px] leading-[120%] font-bold md:text-5xl">
            Online booking — the first step towards your health
          </h1>
          <p className="mb-[100px] w-[400px] text-[16px] leading-[34px] text-white">
            Hold incredible events, share knowledge, build and grow your product, create opportunity
          </p>

          <div className="flex h-[56px] max-w-full items-center overflow-hidden rounded-[16px] bg-white px-[4px] shadow-md">
            <div className="flex items-center gap-[14px] px-4 text-gray-500">
              <SearchIcon />
              <input
                type="text"
                placeholder="Name"
                className="w-full py-3 text-black placeholder-[#6E6E6E] outline-none"
                onChange={(e) => setSearchResult(e.target.value)}
                value={searchResult}
              />
            </div>
            <div className="h-[38px] border-l border-[#046D5F]"></div>
            <div className="flex items-center gap-[14px] px-4 text-gray-500">
              <LocationIcon />
              <input
                type="text"
                placeholder="Location"
                className="w-full py-3 text-black placeholder-[#6E6E6E] outline-none"
              />
            </div>
            <button className="h-[48px] cursor-pointer rounded-[16px] bg-[#046D5F] px-[28px] text-[22px] font-semibold tracking-[3%] text-white transition-all hover:bg-teal-600">
              Search
            </button>
          </div>
          {searchResult && (
            <div className="absolute z-[999] mt-1 w-full rounded-[16px] bg-white text-gray-500 shadow-[0px_10px_40px_0px_#12121226]">
              <DoctorSearchResult searchDoctor={searchResult} />
            </div>
          )}
        </div>

        <div className="flex-shrink-0">
          <Image
            src={images.heroImg}
            alt="Hero Image"
            className="absolute right-[15px] bottom-0 h-[500px] w-[400px] rounded-lg object-cover"
            priority
          />
        </div>
        <div className="relative hidden md:block">
          <div className="relative h-[500px] w-full">
            <Image src={images.heroImg} alt="Hero Image" fill className="object-contain" priority />
          </div>
        </div>
      </div>
    </section>
  )
}
