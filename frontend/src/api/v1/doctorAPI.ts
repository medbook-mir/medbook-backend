import { BaseClient } from '@/api/baseClient'
import { ApiResponseWithContent } from '@/types'
import { DoctorType } from '@/types/doctor-type'
import { AxiosResponse } from 'axios'

const urls = {
  getDoctors: 'api/doctor/list',
  getDoctor: (id: string) => `api/doctor/detail/${id}`
}

export class DoctorAPI {
  constructor(private api: BaseClient) {}

  getDoctors = async () => {
    const result: AxiosResponse<ApiResponseWithContent<DoctorType>> = await this.api.get(urls.getDoctors)

    return result
  }

  getDoctor = async (id: string) => {
    const result: AxiosResponse<ApiResponseWithContent<DoctorType>> = await this.api.get(urls.getDoctor(id))

    return result
  }
}

export default new DoctorAPI(BaseClient.getInstance())
