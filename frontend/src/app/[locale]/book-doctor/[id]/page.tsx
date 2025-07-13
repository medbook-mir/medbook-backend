import { Container } from '@/theme/container'
import { CustomBreadcrumb } from '@/components/ui/breadcrumb'
import ImportantThings from '@/components/doctor/important-things'
import BookDoctorCalendar from '@/components/book-doctor/Calendar'

const BookDoctor = async ({ params }: { params: Promise<{ id: string }> }) => {
  const { id } = await params

  return (
    <div className="pt-[33px]">
      <Container>
        <CustomBreadcrumb
          pages={[
            { title: 'Doctor’s profile', href: `/doctors/${id}/` },
            { title: 'Make an appointment online', href: `/book-doctor/${id}/` }
          ]}
        />
        <div className="border-b border-[#EBEBEB] pb-[24px]">
          <h2 className="mt-[40px] mb-[16px] text-[24px] font-[600] tracking-[0.48px]">Make an appointment online</h2>
          <p className="font-[500] tracking-[0.48px]">Fill in the following fields:</p>
        </div>
        <div className="flex flex-col gap-14 pt-[22px] pb-2.5 md:flex-row md:justify-between">
          <div className="flex flex-1 flex-col gap-8 py-2.5">
            <BookDoctorCalendar />
          </div>
          <div className="flex flex-col gap-4 py-2.5">
            <ImportantThings />
          </div>
        </div>
      </Container>
    </div>
  )
}

export default BookDoctor
