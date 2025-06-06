"use client";

import React from "react";
import { HeroLeftSide } from "./HeroLeftSide";
import Image from "next/image";
import { images } from "@/assets";

const HeroSection = () => {
  return (
    <div className="relative grid grid-cols-1 gap-8 md:grid-cols-2">
      <div className="z-10">
        <HeroLeftSide />
      </div>
      <div className="relative hidden md:block">
        <Image
          src={images.heroImg}
          alt="Hero Image"
          width={600}
          height={400}
          className="object-contain"
          priority
        />
      </div>
    </div>
  );
};

export default HeroSection;
