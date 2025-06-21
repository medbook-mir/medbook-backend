import * as yup from "yup";

const loginSchema = yup.object().shape({
  login: yup.string().required(),
  password: yup.string().required(),
});

export type LoginType = yup.InferType<typeof loginSchema>;

export default loginSchema;
