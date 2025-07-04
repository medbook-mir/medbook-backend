'use client'

import { Form } from 'antd'
import { useTranslations } from 'next-intl'
import { useRouter } from '@/i18n/navigation'
import { GoogleIcon } from '@/utils/icons/social-medias'
import { FilledButton } from '@/components/ui/filled-button'
import DefaultInput from '@/components/ui/default-input'
import PasswordInput from '@/components/ui/password-input'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { getRegisterModal } from '@/redux/selectors/modals'
import { closeModal, openModal } from '@/redux/reducers/modals'
import { RegisterType } from '@/schema/register-schema'
import { useRegister } from '@/hooks/useRegister'
import { Controller, SubmitHandler, useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import registerSchema from '@/schema/register-schema'

const RegisterForm = () => {
  const t = useTranslations('registerPage')
  const isRegisterModalOpen = useAppSelector(getRegisterModal)
  const dispatch = useAppDispatch()
  const router = useRouter()
  const { register } = useRegister()

  const { isPending: isPendingRegister } = register

  const { control, handleSubmit } = useForm<RegisterType>({
    resolver: yupResolver(registerSchema),
    defaultValues: {
      username: '',
      first_name: '',
      last_name: '',
      birthday: '',
      password: '',
      repeat_password: ''
    }
  })

  const onSubmit: SubmitHandler<RegisterType> = (data) => {
    register.mutate(data)
    dispatch(closeModal('registerModal'))
  }

  const handleLogin = () => {
    if (isRegisterModalOpen) {
      dispatch(closeModal('registerModal'))
      dispatch(openModal('loginModal'))
    } else {
      router.push('/login')
    }
  }

  return (
    <div className="flex flex-col gap-6">
      <h3 className="text-[32px] leading-[100%] font-semibold">{t('formTitle')}</h3>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
        <div className="flex flex-col">
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

          <Form.Item label={t('firstName')} required>
            <Controller
              name="first_name"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <DefaultInput
                  {...field}
                  autoComplete="given-name"
                  status={error ? 'error' : ''}
                  placeholder={t('firstNamePlaceholder')}
                />
              )}
            />
          </Form.Item>

          <Form.Item label={t('lastName')} required>
            <Controller
              name="last_name"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <DefaultInput
                  {...field}
                  autoComplete="family-name"
                  status={error ? 'error' : ''}
                  placeholder={t('lastNamePlaceholder')}
                />
              )}
            />
          </Form.Item>

          <Form.Item label={t('birthday')} required>
            <Controller
              name="birthday"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <DefaultInput
                  {...field}
                  type="date"
                  autoComplete="bday"
                  status={error ? 'error' : ''}
                  placeholder={t('birthdayPlaceholder')}
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
                  autoComplete="new-password"
                  status={error ? 'error' : ''}
                  placeholder={t('passwordPlaceholder')}
                />
              )}
            />
          </Form.Item>

          <Form.Item label={t('confirmPassword')} required>
            <Controller
              name="repeat_password"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <PasswordInput
                  {...field}
                  autoComplete="new-password"
                  status={error ? 'error' : ''}
                  placeholder={t('confirmPasswordPlaceholder')}
                />
              )}
            />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <FilledButton className="!py-5" htmlType="submit" loading={isPendingRegister}>
              {t('signUp')}
            </FilledButton>
            <div className="h-[0.5px] w-full bg-[#E5E5E5]" />
            <FilledButton
              className="!py-5"
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

      <div className="flex flex-col gap-5">
        <div className="flex items-center justify-center gap-3 text-[12px] leading-[20px]">
          <p className="text-[#0D0D0D]">{t('alreadyHaveAnAccount')}</p>
          <button onClick={handleLogin} className="!text-[#046D5F]">
            {t('signInNow')}
          </button>
        </div>
        <p className="text-center text-[12px] leading-[16px] font-normal text-[#696969]">© Medvisit 2025</p>
      </div>
    </div>
  )
}

export default RegisterForm
