import { Box, Typography } from "@mui/material";
import Header from "../_components/Header";
import HeroSection from "./components/HeroSection";
import { SolutionsSection } from "./components/SolutionsSection";

export default function HomePage() {
  return (
    <Box p={"20px"}>
      <Box
        sx={{
          backgroundColor: "#00695C",
          padding: { xs: 4, md: "52px 80px" },
          borderRadius: "34px",
          color: "white"
        }}
      >
        <Header />
        <HeroSection />
      </Box>
      <SolutionsSection />
    </Box>
  );
}
