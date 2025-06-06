"use client";

import { useParams, usePathname, useRouter } from "next/navigation";
import { useTranslation } from "react-i18next";
import Image from "next/image";
import { CustomSelect } from "@/components/ui/select";
import { icons } from "@/assets";

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
          fill
          sizes="28px"
          className="object-cover rounded"
        />
      </div>
      <span className="font-semibold">{option.label}</span>
    </div>
  ),
  value: option.value,
}));

export const LangSelect = () => {
  const { i18n } = useTranslation();
  const { lang } = useParams();
  const pathname = usePathname();
  const router = useRouter();

  const handleLangChange = (value: string) => {
    const newPathname = pathname.replace(`/${lang}`, `/${value}`);
    router.replace(newPathname);
    i18n.changeLanguage(value);
    localStorage.setItem("language", value);
  };

  return (
    <CustomSelect
      style={{ width: 100 }}
      value={i18n.language}
      options={renderLangOptions}
      onSelect={handleLangChange}
      className="lang-select"
    />
  );
};
