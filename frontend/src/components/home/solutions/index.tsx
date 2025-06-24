import { Container } from "@/theme/container";
import { solutionsSteps, solutionsTitle } from "./data";

export const SolutionsSection = () => {
  return (
    <section className="py-[132px] px-[104px]">
      <Container>
        <h2 className="text-[48px] leading-[60px] font-bold tracking-[-2%] text-[#0D0D0D] text-center mb-[60px]">
          {solutionsTitle}
        </h2>
        <div className="mx-auto grid gap-[17px] sm:grid-cols-2 lg:grid-cols-4">
          {solutionsSteps.map((step, index) => (
            <div
              key={index}
              className="bg-white px-[24px] w-full h-[226px] rounded-b-[10px] hover:shadow-lg transition-shadow shadow-[0px_10px_40px_0px_#1212121A] border-t-[3px] border-[#046D5F] flex flex-col justify-center"
            >
              <div className="mb-4">{step.icon}</div>
              <h3 className="text-[14px] leading-[28px] tracking-[3%] font-bold mb-2">
                {step.title}
              </h3>
              <p className="text-[12px] text-[#696969]">{step.description}</p>
            </div>
          ))}
        </div>
      </Container>
    </section>
  );
};
