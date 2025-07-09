import '@/utils/yup-locale'
import * as yup from 'yup'

const registerSchema = yup.object().shape({
  username: yup.string().required(),
  first_name: yup.string().required(),
  last_name: yup.string().required(),
  birthday: yup.string().required(),
  password: yup.string().required(),
  repeat_password: yup.string().required()
})

export type RegisterType = yup.InferType<typeof registerSchema>

export default registerSchema
