import { Button, ButtonProps } from "antd";
import { forwardRef, HTMLProps } from "react";
import styled from "styled-components";

interface FilledButtonProps extends ButtonProps {
  children?: React.ReactNode;
  className?: HTMLProps<HTMLElement>["className"];
  bgColor?: string;
}

export const FilledButton = forwardRef<HTMLButtonElement, FilledButtonProps>(
  ({ children, className, bgColor, ...props }, ref) => {
    return (
      <CustomFilledButton
        ref={ref}
        type="primary"
        className={className}
        $bgColor={bgColor}
        {...props}
      >
        {children}
      </CustomFilledButton>
    );
  }
);

FilledButton.displayName = "FilledButton";

export const CustomFilledButton = styled(Button)<{ $bgColor?: string }>`
  background: ${(props) => props.$bgColor || "#046d5f"} !important;
  color: white !important;
  border: none !important;
  font-size: 16px !important;
  font-weight: 500 !important;
  line-height: 24px !important;
  padding: 24px !important;
  border-radius: 6px !important;
  box-shadow: none !important;

  &:hover {
    background: ${(props) => `${props.$bgColor}dd` || "#046d5fdd"} !important;
  }
`;
