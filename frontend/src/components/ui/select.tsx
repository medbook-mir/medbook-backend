import { Select, SelectProps } from "antd";
import styled from "styled-components";

export const CustomSelect: React.FC<SelectProps> = ({ ...props }) => {
  return <ExtendedSelect {...props} />;
};

const ExtendedSelect = styled(Select)`
  /* Basic styles for CustomSelect can be added here if needed */
  /* For now, it will inherit Ant Design's default styles */
`;
