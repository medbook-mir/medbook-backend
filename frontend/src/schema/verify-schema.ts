import '@/utils/yup-locale'
import * as yup from 'yup'

const verifySchema = yup.object().shape({
  email_code: yup.string().required()
})

export type VerifyType = yup.InferType<typeof verifySchema>

export default verifySchema
