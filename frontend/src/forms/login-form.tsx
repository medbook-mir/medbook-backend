"use client";

import { Form, Checkbox } from "antd";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { GoogleIcon } from "@/utils/icons/social-medias";
import { FilledButton } from "@/components/ui/filled-button";
import { LoginBodyType } from "@/types";
import DefaultInput from "@/components/ui/default-input";
import PasswordInput from "@/components/ui/password-input";

const LoginForm = () => {
  const t = useTranslations();
  const [form] = Form.useForm<LoginBodyType>();

  const onSubmit = (values: LoginBodyType) => {
    console.log("Login form submitted:", values);
  };

  return (
    <div className="flex-1 pr-[78px] pl-12 flex flex-col gap-6">
      <h3 className="text-[32px] font-semibold leading-[100%]">
        {t("login.label")}
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
        <div className="flex flex-col pb-5">
          <Form.Item
            label={t("login.label")}
            name="login"
            rules={[
              { required: true, message: "Please input your login!" },
              { type: "email", message: "Please enter a valid email!" },
            ]}
          >
            <DefaultInput
              autoComplete="login"
              placeholder={t("login.loginPlaceholder")}
            />
          </Form.Item>

          <Form.Item
            label={t("login.password")}
            name="password"
            rules={[
              { required: true, message: "Please input your password!" },
              { min: 6, message: "Password must be at least 6 characters!" },
            ]}
          >
            <PasswordInput
              autoComplete="password"
              placeholder={t("login.passwordPlaceholder")}
            />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <div className="flex items-center justify-between">
              <Form.Item name="remember" valuePropName="checked" noStyle>
                <Checkbox>{t("login.rememberMe")}</Checkbox>
              </Form.Item>
              <Link href="/forgot-password">{t("login.forgotPassword")}</Link>
            </div>

            <FilledButton
              className="py-[10px] w-full"
              iconPosition="end"
              htmlType="submit"
            >
              {t("login.signIn")}
            </FilledButton>

            <div className="w-full h-[0.5px] bg-[#E5E5E5]" />

            <FilledButton
              className="py-[10px] w-full"
              iconPosition="start"
              icon={<GoogleIcon />}
              htmlType="submit"
              bgColor="#0D0D0D"
            >
              {t("login.withGoogle")}
            </FilledButton>
          </div>
        </div>
      </Form>

      <div className="flex flex-col gap-10">
        <div className="flex gap-3 items-center text-[12px] leading-[20px] justify-center">
          <p className="text-[#0D0D0D]">{t("login.dontHaveAccount")}</p>
          <Link href="/register">{t("login.signUpNow")}</Link>
        </div>
        <p className="text-center text-[#696969] font-normal text-[12px] leading-[16px]">
          © Medvisit 2025
        </p>
      </div>
    </div>
  );
};

export default LoginForm;
