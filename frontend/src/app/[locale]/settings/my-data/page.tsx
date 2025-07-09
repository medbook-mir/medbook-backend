'use client'

import Image from 'next/image'
import { EditIcon, ProfileAvatarIcon } from '@/utils/icons'
import { FilledButton } from '@/components/ui/filled-button'
import { InfoBlock } from '@/components/settings/info-block'
import { useRouter } from '@/i18n/navigation'
import { useTranslations } from 'next-intl'

const mockMyData = {
  name: 'Shohrux Rahmatov',
  birthday: '27/08/2000',
  email: 'shohrux.rahmatov@gmail.com',
  phone: '+99890 002 6655',
  gender: 'Male',
  photo: ''
}

const MyData = () => {
  const t = useTranslations('settingsLayout.myDataPage')
  const router = useRouter()

  return (
    <div className="flex flex-col p-10">
      <div className="flex items-center justify-between border-b-2 border-[#E9ECF4] pb-5">
        <div className="flex items-center gap-8">
          {mockMyData?.photo ? (
            <Image src={mockMyData?.photo} alt="profile photo" width={120} height={120} />
          ) : (
            <ProfileAvatarIcon />
          )}
          <div className="flex flex-col gap-1">
            <h1 className="text-[24px] leading-8 font-semibold">{mockMyData?.name}</h1>
            <p className="text-[16px] leading-[18px] font-normal text-[#797979]">{t('customer')}</p>
          </div>
        </div>
        <FilledButton
          icon={<EditIcon />}
          className="!w-auto !rounded-2xl !bg-[#F4F6F9] !px-16 !py-6 !leading-[18px] font-normal !text-[#264796]"
          onClick={() => router.push('editing')}
        >
          {t('editProfile')}
        </FilledButton>
      </div>
      <div className="grid grid-cols-2 gap-x-16 gap-y-2 pt-6">
        <InfoBlock title={t('name')} value={mockMyData?.name} />
        <InfoBlock title={t('birthday')} value={mockMyData?.birthday} />
        <InfoBlock title={t('phone')} value={mockMyData?.phone} />
        <InfoBlock title={t('gender')} value={mockMyData?.gender} />
        <InfoBlock title={t('email')} value={mockMyData?.email} />
      </div>
    </div>
  )
}
export default MyData
