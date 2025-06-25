import { useRouter } from "@/i18n/navigation";
import { useAppDispatch } from "@/redux/store";
import { loginThunk } from "@/redux/thunks/authThunk";
import { LoginBodyType } from "@/types";
import { useMutation } from "@/hooks/useQuery";
import { useTranslations } from "next-intl";
import { useCustomNotification } from "./useNotification";
import { TokenService } from "@/utils/storage";

export const useLogin = () => {
  const dispatch = useAppDispatch();
  const router = useRouter();
  const t = useTranslations();
  const { openNotification } = useCustomNotification();
  const login = useMutation({
    mutationFn: async (data: LoginBodyType) => {
      return dispatch(loginThunk(data)).unwrap();
    },
    onError: (err: any) => {
      console.log("err", err);
      openNotification(
        "error",
        `${t("basic.errorsMsg.wrongSomething")}`,
        err?.result.message || `${t("basic.errorsMsg.tryAgain")}`
      );
      router.push("/");
    },
    onSuccess: (data) => {
      TokenService.setToken(
        data.result.accessToken,
        data.result.refreshToken,
        data.result.accessTokenExpiry,
        data.result.refreshTokenExpiry
      );
      // router.push("/admin-panel");
    },
  });
  return { login };
};
