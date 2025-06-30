import Image from 'next/image'
import { StarIcon, VerifiedIcon } from '@/utils/icons/doctor-icons'
import MockDoctorPhoto from '@/assets/mock/doctor_1.png'
import { AvatarIcon } from '@/utils/icons/AvatarIcon'

const mockDoctor = {
  name: 'Kathrin Schenk-Losse',
  verified: true,
  language: 'Uzbek and Russian',
  rating: 4.5,
  photo: MockDoctorPhoto
}

const HeadSection = () => {
  return (
    <section className="flex items-center gap-6 border-b border-[#EBEBEB] pt-10 pb-8">
      <div className="flex h-[132px] w-[120px] items-center justify-center rounded-[16px] bg-[#F3F3F3]">
        {mockDoctor?.photo ? <Image src={mockDoctor.photo} alt="doctor" width={120} height={132} /> : <AvatarIcon />}
      </div>
      <div className="flex h-full flex-col gap-2.5">
        <h3 className="flex items-center gap-2">
          <span className="text-[24px] leading-[100%] font-semibold">{mockDoctor.name}</span>
          {mockDoctor.verified && <VerifiedIcon />}
        </h3>
        <p className="text-[16px] leading-[100%] font-medium text-[#046D5F]">Gynecologist</p>
        <p className="flex items-center gap-2 text-[16px] leading-[100%] font-semibold">
          <span className="text-[#046D5F]">Languages spoken:</span>
          <span>{mockDoctor.language}</span>
        </p>
        <div className="flex h-7 w-[59px] items-center justify-center gap-1 rounded-[8px] bg-[#FFF2E1]">
          <StarIcon />
          <span className="text-[12px] leading-[100%] font-semibold">{mockDoctor.rating}</span>
        </div>
      </div>
    </section>
  )
}

export default HeadSection
