import { Select, SelectProps } from "antd";
import styled from "styled-components";

export const CustomSelect: React.FC<SelectProps> = ({ ...props }) => {
  return <ExtendedSelect {...props} />;
};

const ExtendedSelect = styled(Select)`
  .ant-select-selector {
    border: none !important;
    box-shadow: none !important;
    background-color: transparent !important;
    padding-right: 24px !important;
  }
  .ant-select-arrow {
    color: #046d5f;
    right: 8px !important;
  }
  &.lang-select .ant-select-selection-item {
    display: flex;
    justify-content: center;
    padding-right: 8px;
  }
`;
