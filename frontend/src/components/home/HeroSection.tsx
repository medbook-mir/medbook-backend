"use client";

import { images } from "@/assets";
import { LocationIcon } from "@/utils/icons/LocationIcon";
import { SearchIcon } from "@/utils/icons/SearchIcon";
import Image from "next/image";

export default function HeroSection() {
  return (
    <section className="text-white">
      <div className="max-w-7xl mx-auto flex flex-col-reverse lg:flex-row items-center justify-between gap-10">
        <div>
          <h1 className="text-[56px] md:text-5xl font-bold leading-[120%] mb-6 w-[450px]">
            Online booking — the first step towards your health
          </h1>
          <p className="text-white text-[16px] leading-[34px] mb-[100px] w-[400px]">
            Hold incredible events, share knowledge, build and grow your
            product, create opportunity
          </p>

          <div className="bg-white rounded-[16px] h-[56px] overflow-hidden flex items-center shadow-md max-w-full px-[4px]">
            <div className="flex items-center gap-[14px] px-4 text-gray-500">
              <SearchIcon />
              <input
                type="text"
                placeholder="Name"
                className="outline-none py-3 w-full text-black placeholder-[#6E6E6E]"
              />
            </div>
            <div className="border-l border-[#046D5F] h-[38px]"></div>
            <div className="flex items-center gap-[14px] px-4 text-gray-500">
              <LocationIcon />
              <input
                type="text"
                placeholder="Location"
                className="outline-none py-3 w-full text-black placeholder-[#6E6E6E]"
              />
            </div>
            <button className="bg-[#046D5F] hover:bg-teal-600 text-[22px] tracking-[3%] text-white font-semibold px-[28px] h-[48px] rounded-[16px] transition-all cursor-pointer">
              Search
            </button>
          </div>
        </div>

        <div className="flex-shrink-0">
          <Image
            src={images.heroImg}
            alt="Hero Image"
            className="absolute bottom-0 right-[15px] w-[400px] h-[500px] object-cover rounded-lg"
            priority
          />
        </div>
        <div className="relative hidden md:block">
          <div className="relative h-[500px] w-full">
            <Image
              src={images.heroImg}
              alt="Hero Image"
              fill
              className="object-contain"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  );
}
