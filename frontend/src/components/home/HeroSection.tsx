"use client";

import React from "react";
import { HeroLeftSide } from "./HeroLeftSide";
import Image from "next/image";
import { images } from "@/assets";
import { Container } from "@/theme/container";

const HeroSection = () => {
  return (
    <section className="relative grid grid-cols-1 gap-8 md:grid-cols-2">
      <Container>
        <div className="z-10">
          <HeroLeftSide />
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
      </Container>
    </section>
  );
};

export default HeroSection;
