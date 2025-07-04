import { useTranslations } from 'next-intl'
import { Modal } from 'antd'
import { closeModal } from '@/redux/reducers/modals'
import { getRegisterModal } from '@/redux/selectors/modals'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import RegisterForm from '@/forms/register-form'

const RegisterModal = () => {
  const t = useTranslations()
  const isOpen = useAppSelector(getRegisterModal)

  const dispatch = useAppDispatch()

  const onCloseModal = () => {
    dispatch(closeModal('registerModal'))
  }

  return (
    <Modal centered open={isOpen} onCancel={onCloseModal} width={700} footer>
      <div className="p-6 sm:px-12 sm:py-10">
        <RegisterForm />
      </div>
    </Modal>
  )
}

export default RegisterModal
