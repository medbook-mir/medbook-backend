import '@/utils/yup-locale'
import * as yup from 'yup'

const myDataSchema = yup.object().shape({
  name: yup.string().required(),
  birthday: yup.string().required(),
  phone: yup.string().required(),
  email: yup.string().required(),
  photo: yup.string().required(),
  username: yup.string().required()
})

export type MyDataType = yup.InferType<typeof myDataSchema>

export default myDataSchema
