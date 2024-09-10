import { Navigate } from "react-router-dom";
import { useAuthStore } from "../store/auth";
import Swal from "sweetalert2";

const Toast = Swal.mixin({
   toast: true,
   position: "top",
   showConfirmButton: false,
   timer: 3000,
   timerProgressBar: true,
});


const PrivateRoute = ({ children }) => {
   const isLoggedIn = useAuthStore((state) => state.isLoggedIn)();
   if (!isLoggedIn) {
      // Trigger the toast notification for unauthenticated access
      Toast.fire({
         icon: "warning",
         title: "Login or register to view account details",
      });
      return <Navigate to="/login" />;
   }

   return <>{children}</>;
};

export default PrivateRoute;