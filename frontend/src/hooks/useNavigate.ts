import { useParams, useRouter } from "next/navigation";

const useNavigate = () => {
  const { lang } = useParams();
  const router = useRouter();
  const navigateTo = (path: string) => router.push(`/${lang}/${path}`);
  const replaceTo = (path: string) => router.replace(`/${lang}/${path}`);

  return { navigateTo, replaceTo };
};

export default useNavigate;

export const generateNavigate = (path: string) => {
  const lang = localStorage.getItem("language") || "en";
  return `/${lang}${path}`;
};
