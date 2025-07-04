import { AddressIcon, EmailIcon, ExperienceIcon, PhoneIcon } from '@/utils/icons/doctor-icons'

const mockProfile = {
  description:
    'Dear patients, I am pleased to welcome you to my practice in Solingen. I am available for regular gynecological checkups and to advise you on all matters relating to contraception. Schedule your appointment directly online! My team and I welcome you to our modern practice for gynecology and obstetrics. Through continuous training and human understanding, I aim to make your treatment in my facilities as pleasant as possible and contribute to maintaining your health with the help of innovative treatment methods.',
  info: [
    {
      icon: <EmailIcon />,
      title: 'Mail address',
      value: 'Kathrin.first@example.com'
    },
    {
      icon: <PhoneIcon />,
      title: 'Phone number',
      value: '+998 99 1234567'
    },
    {
      icon: <AddressIcon />,
      title: 'Country',
      value: 'Tashkent, Uzbekistan'
    },
    {
      icon: <ExperienceIcon />,
      title: 'Years of experience',
      value: '5 Years'
    }
  ]
}

const InfoBlock = ({ icon, title, value }: { icon: React.ReactNode; title: string; value: string }) => {
  return (
    <div className="flex items-center gap-2">
      {icon}
      <div className="flex flex-col gap-1">
        <h4 className="text-[16px] leading-[160%] font-medium">{value}</h4>
        <p className="text-[14px] leading-[20px] text-[#515B6F]">{title}</p>
      </div>
    </div>
  )
}

const Profile = () => {
  return (
    <section className="border-b border-[#EBEBEB] pb-8">
      <h2 className="mb-4 text-[20px] leading-[100%] font-semibold">Profile</h2>
      <p className="text-[16px] leading-[160%] text-[#515B6F]">{mockProfile.description}</p>
      <div className="grid grid-cols-1 gap-6 pt-6 sm:grid-cols-2">
        {mockProfile.info.map((data, index) => (
          <InfoBlock key={index} icon={data.icon} title={data.title} value={data.value} />
        ))}
      </div>
    </section>
  )
}

export default Profile
