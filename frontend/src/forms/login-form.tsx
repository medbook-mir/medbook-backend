'use client'

import { Form, Checkbox } from 'antd'
import { useTranslations } from 'next-intl'
import { Link, useRouter } from '@/i18n/navigation'
import { GoogleIcon } from '@/utils/icons/social-medias'
import { FilledButton } from '@/components/ui/filled-button'
import loginSchema, { LoginType } from '@/schema/login-schema'
import DefaultInput from '@/components/ui/default-input'
import PasswordInput from '@/components/ui/password-input'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { getLoginModal } from '@/redux/selectors/modals'
import { closeModal, openModal } from '@/redux/reducers/modals'
import { useLogin } from '@/hooks/useLogin'
import { Controller, SubmitHandler, useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'

const LoginForm = () => {
  const t = useTranslations('loginPage')
  const isLoginModalOpen = useAppSelector(getLoginModal)
  const dispatch = useAppDispatch()
  const router = useRouter()
  const { login } = useLogin()

  const { isPending: isPendingLogin } = login

  const { control, handleSubmit } = useForm<LoginType>({
    resolver: yupResolver(loginSchema),
    defaultValues: {
      username: '',
      password: '',
      remember: false
    }
  })

  const onSubmit: SubmitHandler<LoginType> = (data) => {
    login.mutate(data)
    dispatch(closeModal('loginModal'))
  }

  const handleRegister = () => {
    if (isLoginModalOpen) {
      dispatch(closeModal('loginModal'))
      dispatch(openModal('registerModal'))
    } else {
      router.push('/register')
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <h3 className="text-[32px] leading-[100%] font-semibold">{t('formTitle')}</h3>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
        <div className="flex flex-col pb-5">
          <Form.Item label={t('username')} required>
            <Controller
              name="username"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <DefaultInput
                  {...field}
                  autoComplete="username"
                  status={error ? 'error' : ''}
                  placeholder={t('usernamePlaceholder')}
                />
              )}
            />
          </Form.Item>

          <Form.Item label={t('password')} required>
            <Controller
              name="password"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <PasswordInput
                  {...field}
                  autoComplete="current-password"
                  status={error ? 'error' : ''}
                  placeholder={t('passwordPlaceholder')}
                />
              )}
            />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <div className="flex items-center justify-between">
              <Controller
                name="remember"
                control={control}
                render={({ field }) => (
                  <Checkbox checked={field.value} onChange={(e) => field.onChange(e.target.checked)}>
                    {t('rememberMe')}
                  </Checkbox>
                )}
              />
              <Link href="/forgot-password" className="!text-[#046D5F]">
                {t('forgotPassword')}
              </Link>
            </div>

            <FilledButton className="w-full !py-5" iconPosition="end" htmlType="submit" loading={isPendingLogin}>
              {t('signIn')}
            </FilledButton>

            <div className="h-[0.5px] w-full bg-[#E5E5E5]" />

            <FilledButton
              className="w-full !py-5"
              iconPosition="start"
              icon={<GoogleIcon />}
              htmlType="button"
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
          <button onClick={handleRegister} className="!text-[#046D5F]">
            {t('signUpNow')}
          </button>
        </div>
        <p className="text-center text-[12px] leading-[16px] font-normal text-[#696969]">© Medvisit 2025</p>
      </div>
    </div>
  )
}

export default LoginForm
