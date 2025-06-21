"use client";

import { Form } from "antd";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { GoogleIcon } from "@/utils/icons/social-medias";
import { FilledButton } from "@/components/ui/filled-button";
import { LoginBodyType } from "@/types";
import DefaultInput from "@/components/ui/default-input";
import PasswordInput from "@/components/ui/password-input";

const RegisterForm = () => {
  const t = useTranslations();
  const [form] = Form.useForm<LoginBodyType>();

  const onSubmit = (values: LoginBodyType) => {
    console.log("Login form submitted:", values);
  };

  return (
    <div className="flex-1 pr-[78px] pl-12 flex flex-col gap-6">
      <h3 className="text-[32px] font-semibold leading-[100%]">
        {t("register.formTitle")}
      </h3>
      <Form
        layout="vertical"
        onFinish={onSubmit}
        form={form}
        initialValues={{
          login: "",
          password: "",
        }}
      >
        <div className="flex flex-col">
          <Form.Item
            label={t("register.email")}
            name="login"
            rules={[
              { required: true, message: "Please input your login!" },
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <DefaultInput
              autoComplete="email"
              placeholder={t("register.emailPlaceholder")}
            />
          </Form.Item>
          <Form.Item
            label={t("register.name")}
            name="name"
            rules={[
              { required: true, message: "Please input your login!" },
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <DefaultInput
              autoComplete="name"
              placeholder={t("register.namePlaceholder")}
            />
          </Form.Item>
          <Form.Item
            label={t("register.birthday")}
            name="birthday"
            rules={[
              { required: true, message: "Please input your login!" },
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <DefaultInput
              autoComplete="birthday"
              placeholder={t("register.birthdayPlaceholder")}
            />
          </Form.Item>

          <Form.Item
            label={t("register.password")}
            name="password"
            rules={[
              { required: true, message: "Please input your password!" },
              { min: 6, message: "Password must be at least 6 characters!" },
            ]}
          >
            <PasswordInput
              autoComplete="password"
              placeholder={t("register.passwordPlaceholder")}
            />
          </Form.Item>
          <Form.Item
            label={t("register.password2")}
            name="password2"
            rules={[
              { required: true, message: "Please input your password!" },
              { min: 6, message: "Password must be at least 6 characters!" },
            ]}
          >
            <PasswordInput
              autoComplete="password"
              placeholder={t("register.password2Placeholder")}
            />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <FilledButton htmlType="submit">
              {t("register.signUp")}
            </FilledButton>
            <div className="w-full h-[0.5px] bg-[#E5E5E5]" />
            <FilledButton
              iconPosition="start"
              icon={<GoogleIcon />}
              htmlType="submit"
              bgColor="#0D0D0D"
            >
              {t("register.withGoogle")}
            </FilledButton>
          </div>
        </div>
      </Form>

      <div className="flex flex-col gap-5">
        <div className="flex gap-3 items-center text-[12px] leading-[20px] justify-center">
          <p className="text-[#0D0D0D]">{t("register.alreadyHaveAnAccount")}</p>
          <Link href="/login">{t("register.signInNow")}</Link>
        </div>
        <p className="text-center text-[#696969] font-normal text-[12px] leading-[16px]">
          © Medvisit 2025
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;
