import { useRouter } from '@/i18n/navigation'
import { useAppDispatch } from '@/redux/store'
import { logoutThunk } from '@/redux/thunks/authThunk'
import { useMutation } from '@/hooks/useQuery'
import { useTranslations } from 'next-intl'
import { useCustomNotification } from './useNotification'

export const useLogout = () => {
  const dispatch = useAppDispatch()
  const router = useRouter()
  const t = useTranslations()
  const { openNotification } = useCustomNotification()

  const logout = useMutation({
    mutationFn: async () => {
      return dispatch(logoutThunk()).unwrap()
    },
    onError: (err: any) => {
      console.log('Logout error:', err)
      openNotification(
        'error',
        `${t('basic.errorsMsg.wrongSomething')}`,
        err?.result?.message || err?.message || `${t('basic.errorsMsg.tryAgain')}`
      )
    },
    onSuccess: () => {
      openNotification('success', 'Success', 'Logged out successfully')
      router.push('/')
    }
  })

  return { logout }
}
