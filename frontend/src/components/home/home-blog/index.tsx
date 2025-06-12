import { Container } from "@/theme/container";
import Image from "next/image";
import { cardData } from "./data";
import { Link } from "@/i18n/navigation";
import { RightRedIcon } from "@/utils/icons/arrow-icons";

const HomeBlog = () => {
  return (
    <section className="py-20">
      <Container>
        <div className="max-w-[750px] flex flex-col gap-4 mx-auto text-center mb-[60px]">
          <h1 className="text-[46px] font-bold text-[#0D0D0D] leading-[100%]">
            Blog
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
              className="flex w-[384px] p-6 gap-8 rounded-[25px] border-[2px] border-[#B5B5B580] flex-col"
              key={index}
            >
              <Image src={item.img} alt="Schedule" width={304} height={300} />
              <div className="flex flex-col gap-5">
                <div className="flex flex-col gap-3">
                  <h3 className="text-[16px] font-bold leading-[26px] text-[#222]">
                    {item.title}
                  </h3>
                  <p className="text-[#555] text-[12px] leading-4 font-medium">
                    {item.description}
                  </p>
                </div>
                <div className="flex justify-between items-center">
                  <Link
                    href={item.link}
                    className="flex items-center gap-3 cursor-pointer"
                  >
                    <span className="text-[14px] font-medium leading-6 underline">
                      Learn more
                    </span>
                    <RightRedIcon />
                  </Link>
                  <p className="text-[#555] text-[14px] leading-6 font-normal">
                    {item.date}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
};

export default HomeBlog;
