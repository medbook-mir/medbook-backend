import { MainLogoWhite } from "@/assets/icons/MainLogoWhite";
import { Link } from "@/i18n/navigation";
import { Container } from "@/theme/container";
import { GoogleIcon } from "@/utils/icons/social-medias";

const Login = () => {
  return (
    <Container>
      <div className="py-6 h-screen flex gap-20 items-center">
        <div className="flex h-full flex-1 gap-[136px] flex-col bg-[#046D5F] rounded-4xl px-10 pt-[70px]">
          <Link href="/">
            <MainLogoWhite />
          </Link>
          <div className="flex flex-col gap-11">
            <h2 className="text-white text-[40px] font-medium">
              Online healthcare – Always by your side
            </h2>
            <p className="text-white text-[16px] font-medium">
              Welcome to your personal digital clinic. With just a few clicks,
              you can connect to certified doctors, get professional medical
              advice, and receive prescriptions – all from the comfort of your
              home. Fast, secure, and available 24/7."
            </p>
          </div>
        </div>
        <div className="flex-1 pr-[78px] pl-12 flex flex-col gap-6">
          <h3 className="text-[32px] font-semibold leading-[100%]">Login</h3>

          <div className="flex flex-col gap-4 pb-5">
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Login</label>
              <input type="text" placeholder="Email or phone number" />
            </div>
            <div className="flex flex-col gap-2">
              <label htmlFor="login">Password</label>
              <input type="text" placeholder="Enter password" />
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
                Sign in
              </button>
              <div className="w-full h-[0.5px] bg-[#E5E5E5]" />
              <button className="text-white bg-[#0D0D0D] text-[12px] leading-[20px] flex items-center justify-center gap-2 py-[10px] rounded-[6px]">
                <GoogleIcon /> <span>Or sign in with Google</span>
              </button>
            </div>
          </div>
          <div className="flex flex-col gap-10">
            <div className="flex gap-3 items-center text-[12px] leading-[20px] mb-10 justify-center">
              <p className="text-[#0D0D0D] ">Dont have an account?</p>
              <Link href="/register">Sign up</Link>
            </div>
            <p className="text-center text-[#696969] font-normal text-[12px] leading-[16px]">
              © Medvisit 2025
            </p>
          </div>
        </div>
      </div>
    </Container>
  );
};

export default Login;
