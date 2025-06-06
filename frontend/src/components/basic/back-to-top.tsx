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
        className="fixed bottom-10 right-10 z-30 transition bg-primary rounded-full flex items-center justify-center shadow text-white w-12 h-12"
      >
        <UpOutlined />
      </button>
    )
  );
};
export default BackToTop;
