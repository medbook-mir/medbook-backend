import { Container } from "@/theme/container";
import { CheckHealthIcon } from "@/utils/icons/CheckHealthIcon";
import { ChooseDoctorIcon } from "@/utils/icons/ChooseDoctorIcon";
import { ScheduleIcon } from "@/utils/icons/ScheduleIcon";
import { SolutionsStarIcon } from "@/utils/icons/SolutionsStarIcon";

const title = "Step by step to get your solutions";
const steps = [
  {
    icon: <CheckHealthIcon />,
    title: "Check health complaints",
    description:
      "Check the disease so you can easily choose the right specialist"
  },
  {
    icon: <ChooseDoctorIcon />,
    title: "Choose doctor Specialist",
    description: "Choose a specialist according to your disease complaints"
  },
  {
    icon: <ScheduleIcon />,
    title: "Make a Schedule",
    description:
      "Make a schedule with the doctor concerned so you can start the examination"
  },
  {
    icon: <SolutionsStarIcon />,
    title: "Get your Solutions",
    description:
      "After conducting an examination with a specialist we can help find the right healing method"
  }
];

export const SolutionsSection = () => {
  return (
    <section className="py-[132px] px-[104px]">
      <Container>
        <h2 className="text-[48px] leading-[60px] font-bold tracking-[-2%] text-[#0D0D0D] text-center mb-[60px]">
          {title}
        </h2>
        <div className="mx-auto grid gap-[17px] sm:grid-cols-2 lg:grid-cols-4">
          {steps.map((step, index) => (
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
