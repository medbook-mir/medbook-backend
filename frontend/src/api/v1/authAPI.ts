import { BaseClient } from "@/api/baseClient";
import {
  ApiResponseWithContent,
  LoginResponseType,
  LoginBodyType,
  RegisterBodyType,
} from "@/types";
import { AxiosResponse } from "axios";

const urls = {
  register: "auth-api/v1/auth/register",
  login: "auth-api/v1/auth",
  logout: "auth-api/v1/auth/logout",
};

export class AuthAPI {
  constructor(private api: BaseClient) {}

  register = async (body: RegisterBodyType) => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> =
      await this.api.post(urls.register, body);

    return result;
  };

  login = async (body: LoginBodyType) => {
    const result: AxiosResponse<ApiResponseWithContent<LoginResponseType>> =
      await this.api.post(urls.login, body);

    return result;
  };

  logout = async () => {
    const result = await this.api.post(urls.logout);

    return result;
  };
}

export default new AuthAPI(BaseClient.getInstance());
