import { images } from "@/assets";
import { Container } from "@/theme/container";
import { CheckIcon } from "@/utils/icons/CheckIcon";
import Image from "next/image";
import { DoctorCardList } from "./AvailableDoctors";

export const FindDoctor = () => {
  return (
    <Container>
      <div className="py-[80px] px-[50px] w-full relative">
        <div className="flex flex-col items-start justify-between gap-[26px] w-[645px]">
          <h1 className="text-[48px] font-bold leading-[60px] text-[#0D0D0D]">
            Find the right doctor according to your complaint
          </h1>
          <p className="text-[#696969] text-[14px] leading-[20px] w-[530px]">
            HealthCare.ly is a free, health app that goes beyond matching you
            with doctors. It actively helps you find the right doctor based on
            your medical and personal needs and connects you with your
            HealthCarely community for ongoing support throughout your journey
            to healthier living.
          </p>
          <div>
            <div className="flex items-center gap-[12px] mb-[16px] text-[#121212]">
              <CheckIcon />
              <p>
                100% free app designed to help you find the right doctor for
                you.
              </p>
            </div>
            <div className="flex items-center gap-[12px] text-[#121212]">
              <CheckIcon />
              <p>Available 900 doctors specialist</p>
            </div>
          </div>
          <button className="bg-[#046D5F] font-[500] rounded-[10px] px-[36px] py-[16px] text-[16px] text-white hover:bg-gray-200 transition">
            Search the doctor
          </button>
        </div>
        <div className="absolute right-0 bottom-0 -mr-4 h-full w-[50%]">
          <div className="absolute top-[50px] left-[50px]">
            <DoctorCardList />
          </div>
          <Image
            src={images.searchDoctor}
            alt="search doctor image"
            height={600}
            width={700}
            // fill
            className="object-contain right-0 bottom-0"
            priority
          />
        </div>
      </div>
    </Container>
  );
};
