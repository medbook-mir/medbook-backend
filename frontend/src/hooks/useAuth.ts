import { useAppDispatch } from "@/redux/store";
import { logoutThunk } from "@/redux/thunks/authThunk";

const useAuth = () => {
  const dispatch = useAppDispatch();

  const handleLogout = () => {
    dispatch(logoutThunk());
    window.location.href = "/";
  };

  return { handleLogout };
};

export default useAuth;
