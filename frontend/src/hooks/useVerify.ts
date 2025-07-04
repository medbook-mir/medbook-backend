import { useRouter } from '@/i18n/navigation'
import { useAppDispatch } from '@/redux/store'
import { verifyThunk } from '@/redux/thunks/authThunk'
import { VerifyBodyType } from '@/types'
import { useMutation } from '@/hooks/useQuery'
import { useTranslations } from 'next-intl'
import { useCustomNotification } from './useNotification'
import { TokenService } from '@/utils/storage'

export const useVerify = () => {
  const dispatch = useAppDispatch()
  const router = useRouter()
  const t = useTranslations()
  const { openNotification } = useCustomNotification()

  const verify = useMutation({
    mutationFn: async (data: VerifyBodyType) => {
      return dispatch(verifyThunk(data)).unwrap()
    },
    onError: (err: any) => {
      console.log('Verification error:', err)
      openNotification(
        'error',
        `${t('basic.errorsMsg.wrongSomething')}`,
        err?.result?.message || err?.message || `${t('basic.errorsMsg.tryAgain')}`
      )
    },
    onSuccess: (data) => {
      TokenService.setToken(
        data.result.accessToken,
        data.result.refreshToken,
        data.result.accessTokenExpiry,
        data.result.refreshTokenExpiry
      )
      openNotification('success', 'Success', 'Email verified successfully')
      router.push('/dashboard')
    }
  })

  return { verify }
}
