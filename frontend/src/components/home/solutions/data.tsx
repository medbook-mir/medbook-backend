import { CheckHealthIcon } from '@/utils/icons/CheckHealthIcon'
import { ChooseDoctorIcon } from '@/utils/icons/ChooseDoctorIcon'
import { ScheduleIcon } from '@/utils/icons/ScheduleIcon'
import { SolutionsStarIcon } from '@/utils/icons/SolutionsStarIcon'

export const solutionsSteps = [
  {
    icon: <CheckHealthIcon />,
    title: 'complaints.title',
    description: 'complaints.description'
  },
  {
    icon: <ChooseDoctorIcon />,
    title: 'doctor.title',
    description: 'doctor.description'
  },
  {
    icon: <ScheduleIcon />,
    title: 'schedule.title',
    description: 'schedule.description'
  },
  {
    icon: <SolutionsStarIcon />,
    title: 'solutions.title',
    description: 'solutions.description'
  }
]
