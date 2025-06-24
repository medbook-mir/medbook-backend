import { useTranslations } from "next-intl";
import { Modal } from "antd";
import { closeModal } from "@/redux/reducers/modals";
import { getLoginModal } from "@/redux/selectors/modals";
import { useAppDispatch, useAppSelector } from "@/redux/store";
import LoginForm from "@/forms/login-form";

const LoginModal = () => {
  const t = useTranslations();
  const isOpen = useAppSelector(getLoginModal);

  const dispatch = useAppDispatch();

  const onCloseModal = () => {
    dispatch(closeModal("loginModal"));
  };

  return (
    <Modal centered open={isOpen} onCancel={onCloseModal} width={700} footer>
      <div className="flex size-full flex-col items-center justify-center gap-5 p-14">
        <h1 className="typography-h3 font-bold">{t("login.label")}</h1>
        <LoginForm />
      </div>
    </Modal>
  );
};

export default LoginModal;
