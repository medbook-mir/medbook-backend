import { Modal } from 'antd'
import { closeModal } from '@/redux/reducers/modals'
import { useAppDispatch, useAppSelector } from '@/redux/store'
import { getVerifyModal } from '@/redux/selectors/modals'
import VerifyForm from '@/forms/verify-form'

const VerifyModal = () => {
  const isOpen = useAppSelector(getVerifyModal)

  const dispatch = useAppDispatch()

  const onCloseModal = () => {
    dispatch(closeModal('verifyModal'))
  }

  return (
    <Modal centered open={isOpen} onCancel={onCloseModal} width={700} footer>
      <div className="p-6 sm:px-12 sm:py-10">
        <VerifyForm />
      </div>
    </Modal>
  )
}

export default VerifyModal
