import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const useAuthRedirect = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"));

    if (!user || !user.name || !user.username) {
      navigate("/"); // 🔄 Redirect to login page
    }
  }, [navigate]);
};

export default useAuthRedirect;
