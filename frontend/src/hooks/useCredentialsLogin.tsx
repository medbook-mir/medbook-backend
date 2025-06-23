// import { useRouter } from "@/i18n/navigation";
// import { useAppDispatch } from "@/redux/store";
// import { credentialsLoginThunk } from "@/redux/thunks/credentialsLoginThunk";
import { LoginBodyType } from "@/types";
import { useMutation } from "@tanstack/react-query";
// import { useTranslations } from "next-intl";
// import { useCustomNotification } from "./useNotification";

export const useCredentialsLogin = () => {
  //   const dispatch = useAppDispatch();
  //   const router = useRouter();
  //   const t = useTranslations();
  //   const { openNotification } = useCustomNotification();
  const credentialsLogin = useMutation({
    //   mutationFn: async (data: LoginBodyType) => {
    //     return dispatch(credentialsLoginThunk(data)).unwrap();
    //   },
    //   onError: (err: any) => {
    //     console.log("err", err);
    //     openNotification(
    //       "error",
    //       `${t("errorsMsg.wrongSomething")}`,
    //       err?.result.message || `${t("errorsMsg.tryAgain")}`
    //     );
    //     router.push("/");
    //   },
    //   onSuccess: (data) => {
    //     TokenService.setToken(
    //       data.result.accessToken,
    //       data.result.refreshToken,
    //       data.result.accessTokenExpiry,
    //       data.result.refreshTokenExpiry
    //     );
    //     //   router.push("/admin-panel");
    //   },
  });
  return { credentialsLogin };
};
