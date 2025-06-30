'use client'

import { Form } from 'antd'
import { useTranslations } from 'next-intl'
import { Link } from '@/i18n/navigation'
import { GoogleIcon } from '@/utils/icons/social-medias'
import { FilledButton } from '@/components/ui/filled-button'
import { RegisterFormType } from '@/types'
import DefaultInput from '@/components/ui/default-input'
import PasswordInput from '@/components/ui/password-input'

const RegisterForm = () => {
  const t = useTranslations('registerPage')
  const [form] = Form.useForm<RegisterFormType>()

  const onSubmit = (values: RegisterFormType) => {
    console.log('Login form submitted:', values)
  }

  return (
    <div className="flex flex-1 flex-col gap-6 pr-[78px] pl-12">
      <h3 className="text-[32px] leading-[100%] font-semibold">{t('formTitle')}</h3>
      <Form
        layout="vertical"
        onFinish={onSubmit}
        form={form}
        initialValues={{
          login: '',
          password: ''
        }}
      >
        <div className="flex flex-col">
          <Form.Item
            label={t('email')}
            name="email"
            rules={[
              { required: true, message: 'Please input your login!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <DefaultInput autoComplete="email" placeholder={t('emailPlaceholder')} />
          </Form.Item>
          <Form.Item
            label={t('name')}
            name="name"
            rules={[
              { required: true, message: 'Please input your login!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <DefaultInput autoComplete="name" placeholder={t('namePlaceholder')} />
          </Form.Item>
          <Form.Item
            label={t('birthday')}
            name="birthday"
            rules={[
              { required: true, message: 'Please input your login!' },
              { type: 'email', message: 'Please enter a valid email!' }
            ]}
          >
            <DefaultInput autoComplete="birthday" placeholder={t('birthdayPlaceholder')} />
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
          <Form.Item
            label={t('confirmPassword')}
            name="confirmPassword"
            rules={[
              { required: true, message: 'Please confirm your password!' },
              { min: 6, message: 'Password must be at least 6 characters!' }
            ]}
          >
            <PasswordInput autoComplete="confirmPassword" placeholder={t('confirmPasswordPlaceholder')} />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <FilledButton htmlType="submit">{t('signUp')}</FilledButton>
            <div className="h-[0.5px] w-full bg-[#E5E5E5]" />
            <FilledButton iconPosition="start" icon={<GoogleIcon />} htmlType="submit" bgColor="#0D0D0D">
              {t('withGoogle')}
            </FilledButton>
          </div>
        </div>
      </Form>

      <div className="flex flex-col gap-5">
        <div className="flex items-center justify-center gap-3 text-[12px] leading-[20px]">
          <p className="text-[#0D0D0D]">{t('alreadyHaveAnAccount')}</p>
          <Link href="/login">{t('signInNow')}</Link>
        </div>
        <p className="text-center text-[12px] leading-[16px] font-normal text-[#696969]">© Medvisit 2025</p>
      </div>
    </div>
  )
}

export default RegisterForm
