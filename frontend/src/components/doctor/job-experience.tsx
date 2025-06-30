import { CertificateIcon } from '@/utils/icons/doctor-icons'

const mockData = {
  description:
    'The focus of my work is a trusting relationship – not only when clarifying contraceptive questions and during regular check-ups, which should be performed at least once a year. I am also happy to advise you if you are planning to have children.',
  clinic: 'AKFA MEDLINE',
  mode: 'Full-Time',
  startDate: 'Jun 2019',
  endDate: 'Present',
  address: 'Tashkent, Uzbekistan'
}

const JobExperience = () => {
  const Dot = () => <span className="h-1 w-1 rounded-full bg-[#A8ADB7]" />

  return (
    <section className="border-b border-[#EBEBEB] pb-8">
      <h2 className="text-[20px] leading-[100%] font-semibold">Job expreience</h2>
      <div className="pt-4 pb-3">
        <div className="flex flex-col gap-1.5 text-[16px] leading-[160%] font-normal text-[#515B6F]">
          <div className="flex items-center gap-2">
            <span className="font-medium text-[#25324B]">{mockData.clinic}</span>
            <Dot />
            <span className="">{mockData.mode}</span>
            <Dot />
            <span>{mockData.startDate}</span> - <span>{mockData.endDate} (1y 1m)</span>
          </div>
          <p className="text-[#7C8493]">{mockData.address}</p>
        </div>
      </div>
      <p className="text-[16px] leading-[160%] text-[#515B6F]">{mockData.description}</p>
    </section>
  )
}

export default JobExperience
