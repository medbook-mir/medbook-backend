"use client";

import { useParams, usePathname, useRouter } from "next/navigation";
import { CustomSelect } from "@/components/ui/select";
import { icons } from "@/assets";
import Image from "next/image";

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
  const pathname = usePathname();
  const router = useRouter();

  const handleLangChange = (value: string) => {
    const newPathname = pathname.replace(`/${locale}`, `/${value}`);
    router.push(newPathname);
    localStorage.setItem("language", value);
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
