import React, { createContext, useContext, ReactNode } from "react";
import { notification } from "antd";

type NotificationType = "success" | "info" | "warning" | "error";

interface NotificationContextType {
  openNotification: (
    type: NotificationType,
    message: string,
    description: string
  ) => void;
}

const NotificationContext = createContext<NotificationContextType | null>(null);

export const NotificationProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [api, contextHolder] = notification.useNotification();

  const openNotification = (
    type: NotificationType,
    message: string,
    description: string
  ) => {
    api[type]({
      message,
      description,
      duration: 5,
    });
  };

  return (
    <NotificationContext.Provider value={{ openNotification }}>
      {contextHolder}
      {children}
    </NotificationContext.Provider>
  );
};

export const useCustomNotification = () => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error(
      "useCustomNotification must be used within a NotificationProvider"
    );
  }
  return context;
};
