"use client";

import { useEffect, useState } from "react";
import { UpOutlined } from "@ant-design/icons";

const BackToTop = () => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      setVisible(window.scrollY > 300);
    };

    window.addEventListener("scroll", toggleVisibility);
    return () => window.removeEventListener("scroll", toggleVisibility);
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  return (
    visible && (
      <button
        onClick={scrollToTop}
        className="fixed cursor-pointer bg-[#046D5F] bottom-3 md:bottom-6 text-white right-3 lg:bottom-12 lg:right-12 md:right-6 z-30 transition bg-primary rounded-full flex items-center justify-center shadow  w-12 h-12"
      >
        <UpOutlined />
      </button>
    )
  );
};
export default BackToTop;
