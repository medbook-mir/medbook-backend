import { useRouter } from '@/i18n/navigation'
import { useAppDispatch } from '@/redux/store'
import { registerThunk } from '@/redux/thunks/authThunk'
import { RegisterBodyType } from '@/types'
import { useMutation } from '@/hooks/useQuery'
import { useTranslations } from 'next-intl'
import { useCustomNotification } from './useNotification'
import { TokenService } from '@/utils/storage'

export const useRegister = () => {
  const dispatch = useAppDispatch()
  const router = useRouter()
  const t = useTranslations()
  const { openNotification } = useCustomNotification()
  const register = useMutation({
    mutationFn: async (data: RegisterBodyType) => {
      return dispatch(registerThunk(data)).unwrap()
    },
    onError: (err: any) => {
      console.log('err', err)
      openNotification(
        'error',
        `${t('basic.errorsMsg.wrongSomething')}`,
        err?.result.message || `${t('basic.errorsMsg.tryAgain')}`
      )
      router.push('/')
    },
    onSuccess: (data) => {
      TokenService.setToken(
        data.result.accessToken,
        data.result.refreshToken,
        data.result.accessTokenExpiry,
        data.result.refreshTokenExpiry
      )
    }
  })
  return { register }
}
