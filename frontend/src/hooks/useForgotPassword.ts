import { useAppDispatch } from '@/redux/store'
import { forgotPasswordThunk } from '@/redux/thunks/authThunk'
import { useMutation } from '@/hooks/useQuery'
import { useTranslations } from 'next-intl'
import { useCustomNotification } from './useNotification'

export const useForgotPassword = () => {
  const dispatch = useAppDispatch()
  const t = useTranslations()
  const { openNotification } = useCustomNotification()

  const forgotPassword = useMutation({
    mutationFn: async (email: string) => {
      return dispatch(forgotPasswordThunk(email)).unwrap()
    },
    onError: (err: any) => {
      console.log('Forgot password error:', err)
      openNotification(
        'error',
        `${t('basic.errorsMsg.wrongSomething')}`,
        err?.result?.message || err?.message || `${t('basic.errorsMsg.tryAgain')}`
      )
    },
    onSuccess: (data) => {
      openNotification('success', 'Success', data.message || 'Password reset email sent successfully')
    }
  })

  return { forgotPassword }
}
