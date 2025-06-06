"use client";

import React from "react";
import { ConfigProvider, theme } from "antd";
import { ComponentToken, GlobalToken } from "@/theme";

const AntdProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        components: ComponentToken,
        token: GlobalToken,
      }}
    >
      {children}
    </ConfigProvider>
  );
};

export default AntdProvider;
