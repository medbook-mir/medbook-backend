import { MainLogoWhite } from "@/assets/icons/MainLogoWhite";
import { Link } from "@/i18n/navigation";
import { Container } from "@/theme/container";
import { GoogleIcon } from "@/utils/icons/social-medias";

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
        <div className="flex-1 pr-[78px] pl-12 flex flex-col gap-6">
          <h3 className="text-[32px] font-semibold leading-[100%]">
            Registration
          </h3>

          <div className="flex flex-col gap-4 pb-5">
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Email or phone number</label>
              <input type="text" placeholder="Enter email or phone number " />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Full name</label>
              <input type="text" placeholder="Enter your full name" />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Birthday</label>
              <input type="text" placeholder="Enter your birthday" />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Create password</label>
              <input type="text" placeholder="Create password" />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Repeat password</label>
              <input type="text" placeholder="Repeat password" />
            </div>
            <div className="flex flex-col gap-8">
              <div className="flex items-center justify-between">
                <label>
                  <input type="radio" />
                  Remember me
                </label>
                <Link href="/forgot-password">Forgot password?</Link>
              </div>
              <button className="text-white bg-[#046D5F] text-center text-[15px] leading-[20px] font-bold py-[10px] rounded-[6px]">
                Register
              </button>
              <div className="w-full h-[0.5px] bg-[#E5E5E5]" />
              <button className="text-white bg-[#0D0D0D] text-[12px] leading-[20px] flex items-center justify-center gap-2 py-[10px] rounded-[6px]">
                <GoogleIcon /> <span>Or sign in with Google</span>
              </button>
            </div>
          </div>
          <div className="flex flex-col gap-10">
            <p className="text-center text-[#696969] font-normal text-[12px] leading-[16px]">
              © Medvisit 2025
            </p>
            <div className="flex gap-3 items-center text-[12px] leading-[20px] mb-10 justify-center">
              <p className="text-[#0D0D0D] ">Dont have an account already?</p>
              <Link href="/login">Sign in now</Link>
            </div>
          </div>
        </div>
      </div>
    </Container>
  );
};

export default Register;
