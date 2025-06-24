"use client";

import { usePathname } from "next/navigation";
import Footer from "@/components/footer";

const FooterWrapper = () => {
  const pathname = usePathname();

  const authPaths = ["/login", "/register", "/forgot-password"];

  const isAuthPage = authPaths.some((path) => pathname.includes(path));

  if (isAuthPage) {
    return null;
  }

  return <Footer />;
};

export default FooterWrapper;
