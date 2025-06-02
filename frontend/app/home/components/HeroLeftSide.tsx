import { LocationIcon } from "@/app/_assets/icons/LocationIcon";
import { SearchIcon } from "@/app/_assets/icons/SearchIcon";
import {
  Box,
  Button,
  InputAdornment,
  Stack,
  TextField,
  Typography
} from "@mui/material";

const title = "Online booking — the first step towards your health";
const description =
  "Hold incredible events, share knowledge, build and grow your product, create opportunity";

export const HeroLeftSide = () => {
  return (
    <Box>
      <Box sx={{ maxWidth: 600 }}>
        <Typography
          variant="h3"
          sx={{ fontWeight: 600, marginBottom: "24px", fontSize: "56px" }}
        >
          {title}
        </Typography>
        <Typography
          sx={{
            fontSize: "16px",
            lineHeight: "34px",
            marginBottom: 4,
            width: "418px"
          }}
        >
          {description}
        </Typography>
      </Box>

      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={2}
        sx={{
          backgroundColor: "white",
          borderRadius: "16px",
          padding: "4px",
          maxWidth: 790,
          alignItems: "center"
        }}
      >
        <TextField
          variant="standard"
          placeholder="Name"
          InputProps={{
            disableUnderline: true,
            startAdornment: (
              <InputAdornment position="start" sx={{ marginRight: "14px" }}>
                <SearchIcon />
              </InputAdornment>
            )
          }}
          sx={{
            flex: 1,
            backgroundColor: "white",
            borderRadius: 2,
            paddingX: 1
          }}
        />
        <TextField
          variant="standard"
          placeholder="Location"
          InputProps={{
            disableUnderline: true,
            startAdornment: (
              <InputAdornment position="start" sx={{ marginRight: "14px" }}>
                <LocationIcon />
              </InputAdornment>
            )
          }}
          sx={{
            flex: 1,
            backgroundColor: "white",
            borderRadius: 2,
            paddingX: 1
          }}
        />
        <Button
          variant="contained"
          sx={{
            backgroundColor: "#046D5F",
            color: "white",
            borderRadius: "16px",
            textTransform: "none",
            padding: "11px 28px",
            whiteSpace: "nowrap",
            fontSize: "22px",
            fontWeight: 600,
            lineHeight: 1,
            boxShadow: "none",
            "&:hover": {
              backgroundColor: "#003d33"
            }
          }}
        >
          Search
        </Button>
      </Stack>
    </Box>
  );
};
