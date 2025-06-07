import createNextIntlPlugin from "next-intl/plugin";
import type { NextConfig } from "next";

const withNextIntl = createNextIntlPlugin();

const config: NextConfig = {
  /* config options here */
  images: {
    unoptimized: true,
  },
};

export default withNextIntl(config);
