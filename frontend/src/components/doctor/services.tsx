const mockServices = [
  '3D / 4D ultrasound',
  'acupuncture',
  'Breast cancer screening',
  'Doppler ultrasound',
  'First trimester screening (ETS)',
  'HPV vaccination',
  'Hormonal coil'
]

const Services = () => {
  return (
    <section className="border-b border-[#EBEBEB] pb-8">
      <h2 className="text-[20px] leading-[100%] font-semibold">Range of services and symptoms treated</h2>
      <div className="flex flex-wrap gap-3 pt-6">
        {mockServices.map((service, index) => (
          <div key={index} className="rounded-full bg-[#E7F0FA] px-4 py-1 text-[16px] leading-[160%] text-[#515B6F]">
            {service}
          </div>
        ))}
      </div>
    </section>
  )
}
export default Services
