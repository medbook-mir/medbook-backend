import * as yup from "yup";

const registerSchema = yup.object().shape({
  email: yup.string().email().required(),
  name: yup.string().required(),
  birthday: yup.date().required(),
  password: yup.string().required(),
  confirmPassword: yup.string().required(),
});

export type RegisterType = yup.InferType<typeof registerSchema>;

export default registerSchema;
