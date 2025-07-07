import { Modal } from 'antd'
import { closeModal } from '@/redux/reducers/modals'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { getLoginModal } from '@/redux/selectors/modals'
import LoginForm from '@/forms/login-form'

const LoginModal = () => {
  const isOpen = useAppSelector(getLoginModal)

  const dispatch = useAppDispatch()

  const onCloseModal = () => {
    dispatch(closeModal('loginModal'))
  }

  return (
    <Modal centered open={isOpen} onCancel={onCloseModal} width={700} footer>
      <div className="p-6 sm:px-12 sm:py-10">
        <LoginForm />
      </div>
    </Modal>
  )
}

export default LoginModal
