import * as yup from "yup";

const envSchema = yup.object({
  NODE_ENV: yup.string().oneOf(["development", "production", "test"]),
  NEXT_APP_BASE_URL: yup.string(),
  NEXT_APP_BASE_URL_STAGING: yup.string(),
  NEXT_APP_ENVIRONMENT: yup.string(),
  NEXT_APP_VERSION: yup.string(),
  NEXT_APP_STAGING_HOST: yup.string(),
  NEXT_API_URL: yup.string(),
});

export const env = envSchema.validateSync(process.env, {
  abortEarly: false,
});
