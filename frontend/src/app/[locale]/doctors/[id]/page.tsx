import { Container } from '@/theme/container'
import { CustomBreadcrumb } from '@/components/ui/breadcrumb'
import HeadSection from '@/components/doctor/head-section'
import Services from '@/components/doctor/services'
import ImportantThings from '@/components/doctor/important-things'
import Profile from '@/components/doctor/profile'
import JobExperience from '@/components/doctor/job-experience'
import Certificates from '@/components/doctor/certificates'
import Location from '@/components/doctor/location'

const DoctorsProfile = async ({ params }: { params: Promise<{ id: string }> }) => {
  const { id } = await params

  return (
    <div className="pt-[33px]">
      <Container>
        <CustomBreadcrumb pages={[{ title: 'Doctor’s profile', href: `/doctors/${id}/` }]} />
        <HeadSection />
        <div className="flex flex-col gap-14 pt-[22px] pb-2.5 md:flex-row md:justify-between">
          <div className="flex flex-1 flex-col gap-8 py-2.5">
            <Services />
            <Profile />
            <JobExperience />
            <Certificates />
          </div>
          <div className="flex flex-col gap-4 py-2.5">
            <ImportantThings />
            <Location />
          </div>
        </div>
      </Container>
    </div>
  )
}

export default DoctorsProfile
