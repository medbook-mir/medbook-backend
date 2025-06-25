'use client'

import { useState } from 'react'
import Image from 'next/image'
import { images } from '@/assets'
import { LocationIcon } from '@/utils/icons/LocationIcon'
import { SearchIcon } from '@/utils/icons/SearchIcon'
import DoctorSearchResult from './search-result'
import { Container } from '@/theme/container'

export default function HeroSection() {
  const [searchResult, setSearchResult] = useState('')
  return (
    <section className="rounded-b-[35px] bg-[#046D5F] pt-[67px] pb-[52px]">
      <Container>
        <div className="relative flex-col-reverse items-center justify-between gap-10 text-white lg:flex-row">
          <div className="relative">
            <h1 className="mb-6 w-[450px] text-[56px] leading-[120%] font-bold md:text-5xl">
              Online booking — the first step towards your health
            </h1>
            <p className="mb-[100px] w-[400px] text-[16px] leading-[34px] text-white">
              Hold incredible events, share knowledge, build and grow your product, create opportunity
            </p>

            <div className="flex h-[56px] w-full max-w-[790px] items-center justify-between overflow-hidden rounded-[16px] bg-white px-[4px] shadow-md">
              <div className="flex items-center">
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
              </div>
              <button className="h-[48px] cursor-pointer rounded-[16px] bg-[#046D5F] px-[28px] text-[22px] font-semibold tracking-[3%] text-white transition-all hover:bg-teal-600">
                Search
              </button>
            </div>
            {searchResult && (
              <div className="absolute z-[999] mt-1 w-full max-w-[790px] rounded-[16px] bg-white text-gray-500 shadow-[0px_10px_40px_0px_#12121226]">
                <DoctorSearchResult searchDoctor={searchResult} />
              </div>
            )}
          </div>

          <div className="flex-shrink-0">
            <Image
              src={images.heroImg}
              alt="Hero Image"
              className="absolute right-0 bottom-[-52px] h-[550px] w-[450px] rounded-lg object-cover"
              priority
            />
          </div>
        </div>
      </Container>
    </section>
  )
}
