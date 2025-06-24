import { env } from "@/utils/env";

const Config = {
  isProduction:
    env.NODE_ENV === "production" && env.NEXT_APP_ENVIRONMENT === "production",
  environment: env.NEXT_APP_ENVIRONMENT,
  appVersion: env.NEXT_APP_VERSION,
  baseUrl: env.NEXT_API_URL,
  stagingHost: env.NEXT_APP_STAGING_HOST,
} as const;

export default Config;
