"use client";

import React from "react";

import { HeroLeftSide } from "./HeroLeftSide";

const HeroSection = () => {
  return (
    <>
      <HeroLeftSide />
      <img
        src="/hero-image.png"
        alt="Hero Image"
        width={350}
        height={250}
        style={{ position: "absolute", right: -68, bottom: -52, zIndex: 2 }}
      />
    </>
  );
};

export default HeroSection;
