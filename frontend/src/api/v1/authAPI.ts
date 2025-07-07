import { BaseClient } from '@/api/baseClient'
import {
  ApiResponseWithContent,
  LoginResponseType,
  LoginBodyType,
  RegisterBodyType,
  VerifyBodyType,
  RefreshBodyType
} from '@/types'
import { AxiosResponse } from 'axios'

const urls = {
  register: 'api/auth/send/',
  login: 'api/auth/login/',
  verify: 'api/auth/verify/',
  refresh: 'api/auth/refresh/',
  logout: 'api/auth/logout/'
}

export class AuthAPI {
  constructor(private api: BaseClient) {}

  register = async (body: RegisterBodyType) => {
    console.log(body)
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> = await this.api.post(urls.register, body)

    return result
  }

  login = async (body: LoginBodyType) => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> = await this.api.post(urls.login, body)

    return result
  }

  logout = async () => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> = await this.api.post(urls.logout)

    return result
  }

  verify = async (body: VerifyBodyType) => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> = await this.api.post(urls.verify, body)

    return result
  }

  refresh = async (body: RefreshBodyType) => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> = await this.api.post(urls.refresh, body)

    return result
  }
}

export default new AuthAPI(BaseClient.getInstance())
