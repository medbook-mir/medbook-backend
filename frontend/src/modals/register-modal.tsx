import { useTranslations } from "next-intl";
import { Modal } from "antd";
import { closeModal } from "@/redux/reducers/modals";
import { getLoginModal } from "@/redux/selectors/modals";
import { useAppDispatch, useAppSelector } from "@/redux/store";
import RegisterForm from "@/forms/register-form";

const RegisterModal = () => {
  const t = useTranslations();
  const isOpen = useAppSelector(getLoginModal);

  const dispatch = useAppDispatch();

  const onCloseModal = () => {
    dispatch(closeModal("registerModal"));
  };

  return (
    <Modal centered open={isOpen} onCancel={onCloseModal} width={700} footer>
      <div className="flex size-full flex-col items-center justify-center gap-5 p-14">
        <h1 className="typography-h3 font-bold">{t("register.formTitle")}</h1>
        <RegisterForm />
      </div>
    </Modal>
  );
};

export default RegisterModal;
