'use client'

import { Form, Checkbox } from 'antd'
import { useTranslations } from 'next-intl'
import { Link } from '@/i18n/navigation'
import { GoogleIcon } from '@/utils/icons/social-medias'
import { FilledButton } from '@/components/ui/filled-button'
import { LoginBodyType } from '@/types'
import DefaultInput from '@/components/ui/default-input'
import PasswordInput from '@/components/ui/password-input'

const LoginForm = () => {
  const t = useTranslations('loginPage')
  const [form] = Form.useForm<LoginBodyType>()

  const onSubmit = (values: LoginBodyType) => {
    console.log('Login form submitted:', values)
  }

  return (
    <div className="flex flex-1 flex-col gap-6 pr-[78px] pl-12">
      <h3 className="text-[32px] leading-[100%] font-semibold">{t('label')}</h3>
      <Form
        layout="vertical"
        onFinish={onSubmit}
        form={form}
        initialValues={{
          login: '',
          password: ''
        }}
      >
        <div className="flex flex-col pb-5">
          <Form.Item
            label={t('label')}
            name="login"
            rules={[
              { required: true, message: 'Please input your login!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <DefaultInput autoComplete="login" placeholder={t('loginPlaceholder')} />
          </Form.Item>

          <Form.Item
            label={t('password')}
            name="password"
            rules={[
              { required: true, message: 'Please input your password!' },
              { min: 6, message: 'Password must be at least 6 characters!' }
            ]}
          >
            <PasswordInput autoComplete="password" placeholder={t('passwordPlaceholder')} />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <div className="flex items-center justify-between">
              <Form.Item name="remember" valuePropName="checked" noStyle>
                <Checkbox>{t('rememberMe')}</Checkbox>
              </Form.Item>
              <Link href="/forgot-password" className="text-[#046D5F]">
                {t('forgotPassword')}
              </Link>
            </div>

            <FilledButton className="w-full py-[10px]" iconPosition="end" htmlType="submit">
              {t('signIn')}
            </FilledButton>

            <div className="h-[0.5px] w-full bg-[#E5E5E5]" />

            <FilledButton
              className="w-full py-[10px]"
              iconPosition="start"
              icon={<GoogleIcon />}
              htmlType="submit"
              bgColor="#0D0D0D"
            >
              {t('withGoogle')}
            </FilledButton>
          </div>
        </div>
      </Form>

      <div className="flex flex-col gap-10">
        <div className="flex items-center justify-center gap-3 text-[12px] leading-[20px]">
          <p className="text-[#0D0D0D]">{t('dontHaveAccount')}</p>
          <Link href="/register" className="text-[#046D5F]">
            {t('signUpNow')}
          </Link>
        </div>
        <p className="text-center text-[12px] leading-[16px] font-normal text-[#696969]">© Medvisit 2025</p>
      </div>
    </div>
  )
}

export default LoginForm
