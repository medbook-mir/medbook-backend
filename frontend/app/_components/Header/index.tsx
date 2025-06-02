"use client";

import React from "react";
import Link from "next/link";
import { AppBar, Toolbar, Typography, Button, Box } from "@mui/material";
import { MainLogo } from "@/app/_assets/icons/MainLogo";

const Header = () => {
  return (
    <AppBar
      position="static"
      color="primary"
      sx={{
        backgroundColor: "transparent",
        boxShadow: "none"
      }}
      elevation={1}
    >
      <Toolbar
        sx={{
          justifyContent: "space-between",
          paddingLeft: "0 !important",
          paddingRight: "0 !important",
          paddingBottom: "67px",
          minHeight: "auto !important"
        }}
      >
        <Link href="/" passHref>
          <MainLogo />
        </Link>

        <Box sx={{ display: "flex", gap: 3 }}>
          <Link href="/about" passHref>
            <Button color="inherit">How it works</Button>
          </Link>
          <Link href="/medicals" passHref>
            <Button color="inherit">Medicals</Button>
          </Link>
          <Link href="/blogs" passHref>
            <Button color="inherit">Blogs</Button>
          </Link>
        </Box>

        <Box>
          <Link href="/login" passHref>
            <Button
              variant="outlined"
              color="inherit"
              sx={{
                borderRadius: "62px",
                p: "11px 36px",
                fontSize: "14px",
                fontWeight: 600,
                lineHeight: 1,
                boxShadow: "none",
                textTransform: "none",
                mr: "24px"
              }}
            >
              For doctors
            </Button>
          </Link>
          <Link href="/login" passHref>
            <Button
              variant="contained"
              sx={{
                backgroundColor: "#fff",
                color: "#046D5F",
                borderRadius: "62px",
                p: "11px 36px",
                fontSize: "14px",
                fontWeight: 600,
                lineHeight: 1,
                boxShadow: "none",
                textTransform: "none"
              }}
            >
              Login
            </Button>
          </Link>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
