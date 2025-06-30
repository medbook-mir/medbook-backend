'use client'

import { PersonIcon, LikeIcon, LocationIcon } from '@/utils/icons/doctor-icons'
import { FilledButton } from '../ui/filled-button'
import { useState } from 'react'

const ImportantThings = () => {
  const [isLiked, setIsLiked] = useState(false)

  return (
    <section className="flex max-w-[350px] flex-col gap-4 rounded-[12px] bg-[#F2F7F6] p-5">
      <h3 className="max-w-[230px] text-[16px] leading-[100%] font-bold">The most important things at a glance</h3>
      <div className="flex items-center gap-3">
        <div className="shrink-0">
          <LocationIcon />
        </div>
        <span className="text-[14px] leading-[100%] font-normal">
          Tashkent, Chilanzar, Bunyodkor street 12/4 home 2A
        </span>
      </div>
      <div className="flex items-center gap-3">
        <div className="shrink-0">
          <PersonIcon />
        </div>
        <span className="text-[14px] leading-[100%] font-normal">
          Contact your facility for simple inquiries outside of an appointment.
        </span>
      </div>
      <div className="flex items-center gap-3">
        <div className="shrink-0">
          <PersonIcon />
        </div>
        <span className="text-[14px] leading-[100%] font-normal">Online booking also possible for new patients</span>
      </div>
      <div className="flex items-center gap-4">
        <FilledButton className="!rounded-full !p-5">Book now</FilledButton>
        <div className="inline-block shrink-0 cursor-pointer" onClick={() => setIsLiked(!isLiked)}>
          <LikeIcon fill={isLiked ? '#f00' : '#CDCDCD'} />
        </div>
      </div>
    </section>
  )
}
export default ImportantThings
