import { Box, Typography } from "@mui/material";

const title = "Step by step to get your solutions";

export const SolutionsSection = () => {
  return (
    <Box sx={{ p: "132px 120px" }}>
      <Typography
        variant="h2"
        sx={{
          color: "text.primary",
          fontWeight: 700,
          letterSpacing: "-2px",
          marginBottom: "24px",
          fontSize: "48px",
          lineHeight: "60px",
          textAlign: "center",
          pb: "60px"
        }}
      >
        {title}
      </Typography>
    </Box>
  );
};
