import { Spin } from "antd";

type InputSuffixLoadingProps = {
  isLoading?: boolean;
};

const InputSuffixLoading = ({ isLoading = false }: InputSuffixLoadingProps) => {
  return <Spin size="small" spinning={isLoading} />;
};

export default InputSuffixLoading;
