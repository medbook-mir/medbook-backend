'use client'

import { Form } from 'antd'
import { useTranslations } from 'next-intl'
import { useRouter } from '@/i18n/navigation'
import { FilledButton } from '@/components/ui/filled-button'
import DefaultInput from '@/components/ui/default-input'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { closeModal, openModal } from '@/redux/reducers/modals'
import verifySchema, { VerifyType } from '@/schema/verify-schema'
import { Controller, SubmitHandler, useForm } from 'react-hook-form'
import { yupResolver } from '@hookform/resolvers/yup'
import { getVerifyModal } from '@/redux/selectors/modals'
import { useVerify } from '@/hooks/useVerify'

const VerifyForm = () => {
  const t = useTranslations('verifyPage')
  const isVerifyModalOpen = useAppSelector(getVerifyModal)
  const dispatch = useAppDispatch()
  const router = useRouter()
  const { verify } = useVerify()

  const { control, handleSubmit } = useForm<VerifyType>({
    resolver: yupResolver(verifySchema),
    defaultValues: {
      email_code: ''
    }
  })

  const onSubmit: SubmitHandler<VerifyType> = (data) => {
    verify.mutate(data)
    dispatch(closeModal('verifyModal'))
  }

  const handleLogin = () => {
    if (isVerifyModalOpen) {
      dispatch(closeModal('verifyModal'))
      dispatch(openModal('loginModal'))
    } else {
      router.push('/login')
    }
  }

  return (
    <div className="flex flex-col gap-8">
      <h3 className="text-[32px] leading-[100%] font-semibold">{t('formTitle')}</h3>
      <Form layout="vertical" onFinish={handleSubmit(onSubmit)}>
        <div className="flex flex-col">
          <Form.Item label={t('emailCode')} required>
            <Controller
              name="email_code"
              control={control}
              render={({ field, fieldState: { error } }) => (
                <DefaultInput
                  {...field}
                  autoComplete="email_code"
                  status={error ? 'error' : ''}
                  placeholder={t('emailCodePlaceholder')}
                />
              )}
            />
          </Form.Item>

          <div className="flex flex-col gap-8">
            <FilledButton className="!py-5" htmlType="submit" loading={verify.isPending}>
              {t('verify')}
            </FilledButton>
            <div className="h-[0.5px] w-full bg-[#E5E5E5]" />
            <FilledButton className="!py-5" htmlType="button" bgColor="#0D0D0D">
              {t('resendCode')}
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

export default VerifyForm
