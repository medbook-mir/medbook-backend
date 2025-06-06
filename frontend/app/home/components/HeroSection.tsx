"use client";

import React from "react";
import { Box } from "@mui/material";
import { HeroLeftSide } from "./HeroLeftSide";

const HeroSection = () => {
  return (
    <Box position="relative">
      <HeroLeftSide />
      <img
        src="/hero-image.png"
        alt="Hero Image"
        width={350}
        height={250}
        style={{ position: "absolute", right: -68, bottom: -52, zIndex: 2 }}
      />
    </Box>
  );
};

export default HeroSection;
