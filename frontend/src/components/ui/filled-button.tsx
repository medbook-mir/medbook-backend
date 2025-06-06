import { Button, ButtonProps } from "antd";
import { forwardRef, HTMLProps } from "react";
import styled from "styled-components";

interface FilledButtonProps extends ButtonProps {
  children?: React.ReactNode;
  className?: HTMLProps<HTMLElement>["className"];
}

export const FilledButton = forwardRef<HTMLButtonElement, FilledButtonProps>(
  ({ children, className, ...props }, ref) => {
    return (
      <CustomFilledButton
        ref={ref}
        type="primary"
        className={`px-12 py-6 ${className}`}
        {...props}
      >
        {children}
      </CustomFilledButton>
    );
  }
);

FilledButton.displayName = "FilledButton";

export const CustomFilledButton = styled(Button)`
  background: #046d5f;
  color: white !important;
  border: none;
  font-size: 16px;
  font-weight: 500;
  line-height: 120%;

  &:hover {
    background: #046d5fdd !important;
  }
`;
