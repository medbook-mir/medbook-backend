"use client";

import { Container } from "@/theme/container";
import { LangSelect } from "../shared/lang-select";
import Link from "next/link";
import { useParams } from "next/navigation";

const Header = () => {
  const { locale } = useParams();

  return (
    <header className="sticky top-0 z-50 border-b bg-white">
      <Container>
        <div className="flex h-20 items-center justify-between">
          <Link href={`/${locale}`} className="text-xl font-bold text-primary">
            MedVisit
          </Link>
          <div className="flex items-center gap-6">
            <LangSelect />
          </div>
        </div>
      </Container>
    </header>
  );
};

export default Header;
