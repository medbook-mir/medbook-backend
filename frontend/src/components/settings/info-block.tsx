export const InfoBlock = ({ title, value }: { title: string; value: string }) => {
  return (
    <div className="flex flex-col gap-1 pt-5">
      <p className="text-[14px] leading-[16px]">{title}</p>
      <h5 className="text-[16px] leading-[20px] font-semibold">{value}</h5>
    </div>
  )
}
