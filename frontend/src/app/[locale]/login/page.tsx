import { useTranslations } from "next-intl";
import { MainLogoWhite } from "@/assets/icons/MainLogoWhite";
import LoginForm from "@/forms/login-form";
import { Link } from "@/i18n/navigation";
import { Container } from "@/theme/container";

const Login = () => {
  const t = useTranslations();
  return (
    <Container>
      <div className="py-6 h-screen flex gap-20 items-center">
        <div className="flex h-full flex-1 gap-[136px] flex-col bg-[#046D5F] rounded-4xl px-10 pt-[70px]">
          <Link href="/">
            <MainLogoWhite />
          </Link>
          <div className="flex flex-col gap-11">
            <h2 className="text-white text-[40px] font-medium">
              {t("login.title")}
            </h2>
            <p className="text-white text-[16px] font-medium">
              {t("login.description")}
            </p>
          </div>
        </div>
        <LoginForm />
      </div>
    </Container>
  );
};

export default Login;
