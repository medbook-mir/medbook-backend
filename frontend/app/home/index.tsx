import { Box, Typography } from "@mui/material";

export default function HomePage() {
  return (
    <Box>
      <Typography variant="h1" component="h1" gutterBottom>
        Welcome to the Next.js App
      </Typography>
      <Typography variant="body1" gutterBottom>
        This is a simple example of a Next.js application using Material-UI for
        styling.
      </Typography>
    </Box>
  );
}
