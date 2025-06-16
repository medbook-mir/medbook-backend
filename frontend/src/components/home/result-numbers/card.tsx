const ResultNumberCard = ({
  title,
  value,
}: {
  title: string;
  value: number;
}) => {
  return (
    <div className="bg-[#046D5F] py-8 px-10 rounded-[35px] w-[286px] h-[164px] text-white flex flex-col justify-between">
      <h3 className="text-[48px] leading-[60px] font-semibold">{value}+</h3>
      <p className="text-[20px] leading-[30px] font-normal">{title}</p>
    </div>
  );
};
export default ResultNumberCard;
