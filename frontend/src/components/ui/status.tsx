const statuses = {
  canceled: {
    color: 'text-[#FF0000]',
    backgroundColor: 'bg-[#FF424233]',
    text: 'Canceled'
  },
  success: {
    color: 'text-[#008000]',
    backgroundColor: 'bg-[#22B57333]',
    text: 'Success'
  }
}

type StatusProps = {
  status: 'canceled' | 'success'
}

export const Status = ({ status }: StatusProps) => (
  <div
    className={`${statuses[status].color} ${statuses[status].backgroundColor} w-[100px] rounded-[100px] px-4 py-2 text-center text-[14px] leading-[16px] font-semibold`}
  >
    {statuses[status].text}
  </div>
)
