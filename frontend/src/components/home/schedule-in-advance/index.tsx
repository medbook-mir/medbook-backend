import { Container } from "@/theme/container";
import Image from "next/image";
import { cardData } from "./data";

const ScheduleInAdvance = () => {
  return (
    <section className="py-[132px]">
      <Container>
        <div className="max-w-[750px] flex flex-col gap-4 mx-auto text-center mb-[60px]">
          <h1 className="text-[46px] font-bold text-[#0D0D0D] leading-[100%]">
            Make a schedule in advance with the available doctor
          </h1>
          <p className="text-[20px] font-normal leading-7 text-[#565656]">
            Lorem ipsum dolor sit amet consectetur. Orci malesuada mi et mi
            pellentesque tincidunt at mollis facilisis. Nisl eu blandit nunc
            parturient adipiscing commodo.
          </p>
        </div>
        <div className="flex gap-8 justify-center items-center flex-wrap">
          {cardData.map((item, index) => (
            <div
              className={`flex w-[352px] p-6 gap-8 rounded-[25px] border-[2px] border-[#046D5F80] ${index === 1 ? "flex-col-reverse" : "flex-col"}`}
              key={index}
            >
              <Image src={item.img} alt="Schedule" width={304} height={300} />
              <div className="flex flex-col gap-3">
                <h3 className="text-[26px] font-semibold leading-9 text-[#0D0D0D]">
                  {item.title}
                </h3>
                <p className="text-[#808080] text-[16px] leading-6 font-normal">
                  {item.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
};
export default ScheduleInAdvance;
