import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  async redirects() {
    return [
      {
        source: "/",
        destination: "/en",
        permanent: false,
      },
    ];
  },
  images: {
    unoptimized: true,
  },
  async headers() {
    return [
      {
        source: "/.well-known/:path*",
        headers: [
          {
            key: "Content-Type",
            value: "application/json",
          },
          {
            key: "Access-Control-Allow-Origin",
            value: "*",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
