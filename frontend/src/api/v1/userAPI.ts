import { BaseClient } from "@/api/baseClient";
import { ApiResponseWithContent } from "@/types";
import { UserType } from "@/types/user-type";
import { AxiosResponse } from "axios";

const urls = {
  getMe: "auth-api/v1/user/me",
};

export class UserAPI {
  constructor(private api: BaseClient) {}

  getMe = async () => {
    const result: AxiosResponse<ApiResponseWithContent<UserType>> =
      await this.api.get(urls.getMe);

    return result;
  };
}

export default new UserAPI(BaseClient.getInstance());
