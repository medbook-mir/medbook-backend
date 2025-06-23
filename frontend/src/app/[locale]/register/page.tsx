import { MainLogoWhite } from "@/assets/icons/MainLogoWhite";
import { Link } from "@/i18n/navigation";
import { Container } from "@/theme/container";
import RegisterForm from "@/forms/register-form";

const Register = () => {
  return (
    <Container>
      <div className="py-6 h-screen flex gap-20 items-center">
        <div className="flex h-full flex-1 gap-[136px] flex-col bg-[#046D5F] rounded-4xl px-10 pt-[70px]">
          <Link href="/">
            <MainLogoWhite />
          </Link>
          <div className="flex flex-col gap-11">
            <h2 className="text-white text-[40px] font-medium">
              Sign Up and Connect with Trusted Medical Experts
            </h2>
            <p className="text-white text-[16px] font-medium">
              Creating your account gives you access to a world of expert
              medical care, 24/7 consultations, and the freedom to take control
              of your health from anywhere – safely, securely, and
              conveniently."
            </p>
          </div>
        </div>
        <RegisterForm />
      </div>
    </Container>
  );
};

export default Register;
