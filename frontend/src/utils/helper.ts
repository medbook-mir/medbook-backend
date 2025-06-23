import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const mockDoctors = [
  {
    id: 1,
    name: 'Kathrin Schenk-Losse',
    specialty: 'Gynecologist',
    location: 'Tashkent, Chilanzar, Bunyodkor street 12/4 home 2A',
    rating: 4.5,
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
  },
  {
    id: 2,
    name: 'Jane Doe',
    specialty: 'Cardiologist',
    location: 'Tashkent, Yakkasaray, Shota Rustaveli 33',
    rating: 4.8,
    avatar: 'https://randomuser.me/api/portraits/women/65.jpg'
  },
  {
    id: 3,
    name: 'Emily White',
    specialty: 'Neurologist',
    location: 'Tashkent, Yunusabad, Buyuk Ipak Yuli 7',
    rating: 3,
    avatar: 'https://randomuser.me/api/portraits/women/12.jpg'
  }
]
