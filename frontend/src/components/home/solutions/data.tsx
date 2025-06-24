import { CheckHealthIcon } from "@/utils/icons/CheckHealthIcon";
import { ChooseDoctorIcon } from "@/utils/icons/ChooseDoctorIcon";
import { ScheduleIcon } from "@/utils/icons/ScheduleIcon";
import { SolutionsStarIcon } from "@/utils/icons/SolutionsStarIcon";

export const solutionsTitle = "Step by step to get your solutions";

export const solutionsSteps = [
  {
    icon: <CheckHealthIcon />,
    title: "Check health complaints",
    description:
      "Check the disease so you can easily choose the right specialist",
  },
  {
    icon: <ChooseDoctorIcon />,
    title: "Choose doctor Specialist",
    description: "Choose a specialist according to your disease complaints",
  },
  {
    icon: <ScheduleIcon />,
    title: "Make a Schedule",
    description:
      "Make a schedule with the doctor concerned so you can start the examination",
  },
  {
    icon: <SolutionsStarIcon />,
    title: "Get your Solutions",
    description:
      "After conducting an examination with a specialist we can help find the right healing method",
  },
];
