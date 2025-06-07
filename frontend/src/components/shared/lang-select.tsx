"use client";

import { useParams } from "next/navigation";
import { CustomSelect } from "@/components/ui/select";
import { icons } from "@/assets";
import Image from "next/image";
import { useRouter } from "@/i18n/navigation";
import { i18nConfig } from "@/i18n/config";

const langOptions = [
  { icon: icons.en, label: "En", value: "en" },
  { icon: icons.uz, label: "Uz", value: "uz" },
  { icon: icons.ru, label: "Ру", value: "ru" },
];

const renderLangOptions = langOptions.map((option) => ({
  label: (
    <div className="flex items-center gap-2">
      <div className="relative h-5 w-7">
        <Image
          src={option.icon}
          alt={`${option.value} flag`}
          className="h-full w-full rounded object-cover"
          width={20}
          height={20}
        />
      </div>
      <span className="font-semibold">{option.label}</span>
    </div>
  ),
  value: option.value,
}));

export const LangSelect = () => {
  const { locale } = useParams();
  const router = useRouter();

  const handleLangChange = (value: string) => {
    if (!i18nConfig.locales.includes(value as any)) {
      console.error(`Invalid locale: ${value}`);
      return;
    }

    try {
      router.replace("/", { locale: value });
      localStorage.setItem("language", value);
    } catch (error) {
      console.error("Failed to change language:", error);
    }
  };

  return (
    <CustomSelect
      style={{ width: 100 }}
      value={locale}
      options={renderLangOptions}
      onSelect={handleLangChange}
      className="lang-select"
    />
  );
};
