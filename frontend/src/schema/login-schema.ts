import '@/utils/yup-locale'
import * as yup from 'yup'

const loginSchema = yup.object().shape({
  username: yup.string().required(),
  password: yup.string().required(),
  remember: yup.boolean().optional().default(false)
})

export type LoginType = yup.InferType<typeof loginSchema>

export default loginSchema
