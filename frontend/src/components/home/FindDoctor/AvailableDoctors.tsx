import { images } from "@/assets";
import Image from "next/image";

type Doctor = {
  id: number;
  name: string;
  specialty: string;
  image: any;
};

const doctors: Doctor[] = [
  {
    id: 1,
    name: "Dr. Adinda",
    specialty: "Eye Specialist",
    image: images.mockDoctorImage
  },
  {
    id: 2,
    name: "Dr. Jackson",
    specialty: "Ear Specialist",
    image: images.mockDoctorImage
  }
];

export const DoctorCardList = () => {
  return (
    <div className="w-[200px] bg-white rounded-[10px] shadow-[-4px_-10px_50px_0px_#1212121A] px-[30px] py-[18px] flex flex-col gap-4">
      <div>
        <h3 className="text-[#121212] font-semibold text-[16px]">
          Available Doctors
        </h3>
        <p className="text-[#7D7D7D] text-[14px]">Select Doctors</p>
      </div>

      {doctors.map((doctor) => (
        <div key={doctor.id} className="flex items-center gap-3 cursor-pointer">
          <Image
            src={doctor.image}
            alt={doctor.name}
            width={46}
            height={46}
            className="rounded-full"
          />
          <div>
            <p className="text-[#121212] font-semibold text-[14px]">
              {doctor.name}
            </p>
            <p className="text-[#7D7D7D] text-[12px]">{doctor.specialty}</p>
          </div>
        </div>
      ))}

      <button className="w-full mt-2 bg-[#F1F5FF] text-[#046D5F] text-[14px] font-medium py-2 rounded-[10px] hover:bg-[#e0ebff] transition cursor-pointer">
        Find Doctor
      </button>
    </div>
  );
};
