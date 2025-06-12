import { Container } from "@/theme/container";
import { cardData } from "./data";
import ResultNumberCard from "./card";

const ResultNumbers = () => {
  return (
    <section className="py-[132px]">
      <Container>
        <div className="max-w-[750px] flex flex-col gap-4 mx-auto text-center mb-[60px]">
          <h1 className="text-[46px] font-bold text-[#0D0D0D] leading-[100%]">
            We’re employee benefit at  7500+ hospital
          </h1>
          <p className="text-[20px] font-normal leading-7 text-[#565656]">
            Effective progress tracking and milestone setting are critical
            components of any successful project or personal goal. By
            systematically monitoring our achievements.
          </p>
        </div>
        <div className="flex gap-8 justify-center items-center flex-wrap">
          {cardData.map((item, index) => (
            <ResultNumberCard
              key={index}
              title={item.title}
              value={item.value}
            />
          ))}
        </div>
      </Container>
    </section>
  );
};
export default ResultNumbers;
