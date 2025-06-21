import { forwardRef } from "react";
import { type RadioChangeEvent, Radio } from "antd";
import { useTranslations } from "next-intl";

interface RadioInputProps {
  label: string;
  onChange: (e: RadioChangeEvent) => void;
  variants: { value: string; title: string }[];
  defaultValue: string;
  className?: string;
}

const RadioInput = forwardRef<any, RadioInputProps>(
  ({ label, onChange, variants, defaultValue, className }, ref) => {
    const t = useTranslations();

    return (
      <Radio.Group
        onChange={onChange}
        ref={ref}
        className={`${className} w-full`}
        defaultValue={defaultValue}
      >
        <h3>{t(label)}</h3>
        {variants.map((v, i) => (
          <Radio key={i} value={v.value}>
            {t(v.title)}
          </Radio>
        ))}
      </Radio.Group>
    );
  }
);

export default RadioInput;
