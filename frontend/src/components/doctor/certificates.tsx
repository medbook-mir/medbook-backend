import { CertificateIcon } from '@/utils/icons/doctor-icons'

const mockData = {
  orientation: 'Gynecologist',
  task: 'First trimester screening (ETS)',
  issued: 'June 2025',
  certificationId: '046445'
}

const Certificates = () => {
  const Dot = () => <span className="h-1 w-1 rounded-full bg-[#A8ADB7]" />

  return (
    <section className="border-b border-[#EBEBEB] pb-8">
      <h2 className="mb-7 text-[20px] leading-[100%] font-semibold">Certificates</h2>
      <div className="flex gap-4 pt-4 pb-3">
        <CertificateIcon />
        <div className="text-[16px] leading-[160%]">
          <h3 className="mb-3 text-[18px] font-bold">{mockData.orientation}</h3>
          <div className="flex items-center gap-2">
            <span className="font-medium">{mockData.orientation}</span>
            <Dot />
            <span className="font-normal">{mockData.task}</span>
          </div>
          <p className="py-2">Issued: {mockData.issued}</p>
          <p>Certification ID: {mockData.certificationId}</p>
        </div>
      </div>
    </section>
  )
}

export default Certificates
