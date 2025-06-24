"use client";

import { usePathname } from "next/navigation";
import Footer from "@/components/footer";

const FooterWrapper = () => {
  const pathname = usePathname();

  // Hide footer on login and register pages
  const hideFooterPaths = ["/login", "/register", "/forgot-password"];
  const shouldHideFooter = hideFooterPaths.some((path) =>
    pathname.includes(path)
  );

  if (shouldHideFooter) {
    return null;
  }

  return <Footer />;
};

export default FooterWrapper;
