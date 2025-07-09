import { useRouter } from '@/i18n/navigation'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { registerThunk } from '@/redux/thunks/authThunk'
import { RegisterBodyType } from '@/types'
import { useMutation } from '@/hooks/useQuery'
import { useTranslations } from 'next-intl'
import { useCustomNotification } from './useNotification'
import { closeModal, openModal } from '@/redux/reducers/modals'
import { getRegisterModal } from '@/redux/selectors/modals'

export const useRegister = () => {
  const dispatch = useAppDispatch()
  const router = useRouter()
  const t = useTranslations()
  const { openNotification } = useCustomNotification()
  const isRegisterModalOpen = useAppSelector(getRegisterModal)

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
    onSuccess: () => {
      if (isRegisterModalOpen) {
        dispatch(closeModal('registerModal'))
        dispatch(openModal('verifyModal'))
      } else {
        router.push('/verify')
      }
    }
  })
  return { register }
}
