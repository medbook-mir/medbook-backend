const ResultNumberCard = ({ title, value }: { title: string; value: number }) => {
  return (
    <div
      data-aos="fade-left"
      className="flex h-[164px] w-[286px] flex-col justify-between rounded-[35px] bg-[#046D5F] px-10 py-8 text-white"
    >
      <h3 className="text-[48px] leading-[60px] font-semibold">{value}+</h3>
      <p className="text-[20px] leading-[30px] font-normal">{title}</p>
    </div>
  )
}
export default ResultNumberCard
