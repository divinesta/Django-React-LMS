import { useState, useEffect } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import apiInstance from "../../utils/axios";
import Swal from "sweetalert2";

const Toast = Swal.mixin({
   toast: true,
   position: "top",
   showConfirmButton: false,
   timer: 3000,
   timerProgressBar: true,
});


function CreateNewPassword() {
   const navigate = useNavigate();
   const [password, setPassword] = useState("");
   const [confirmpassword, setConfirmPassword] = useState("");
   const [isLoading, setIsLoading] = useState(false);
   // const [error, setError] = useState(null);

   const [searchParam] = useSearchParams();
   const otp = searchParam.get("otp");
   const uidb64 = searchParam.get("uidb64");
   const refresh_token = searchParam.get("refresh_token");

   const handlePasswordSubmit = async (e) => {
      e.preventDefault();
      setIsLoading(true);
      if (password !== confirmpassword) {
         Toast.fire({
            icon: "error",
            title: "Password does not match",
         });
         setIsLoading(false);
      } else {
         const formdata = new FormData();
         formdata.append("password", password);
         formdata.append("otp", otp);
         formdata.append("uidb64", uidb64);
         formdata.append("refresh_token", refresh_token);

         try {
            await apiInstance
               .post(`user/password-change/`, formdata)
               .then((res) => {
                  console.log(res.data);
                  Toast.fire({
                     icon: "success",
                     title: "Password Changed Successfully",
                  });
                  navigate("/login");
                  setIsLoading(false);
               });
         } catch (error) {
            console.log(error);
            Toast.fire({
               icon: "error",
               title: "An error occured while trying to change the password",
            });
            setIsLoading(false);
         }
      }
   };

   return (
      <>
         <BaseHeader />

         <section
            className="container d-flex flex-column vh-100"
            style={{ marginTop: "150px" }}
         >
            <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
               <div className="col-lg-5 col-md-8 py-8 py-xl-0">
                  <div className="card shadow">
                     <div className="card-body p-6">
                        <div className="mb-4">
                           <h1 className="mb-1 fw-bold">Create New Password</h1>
                           <span>Choose a new password for your account</span>
                        </div>
                        <form
                           className="needs-validation"
                           noValidate=""
                           onSubmit={handlePasswordSubmit}
                        >
                           <div className="mb-3">
                              <label htmlFor="password" className="form-label">
                                 Enter New Password
                              </label>
                              <input
                                 type="password"
                                 id="password"
                                 className="form-control"
                                 name="password"
                                 placeholder="**************"
                                 required
                                 onChange={(e) => setPassword(e.target.value)}
                              />
                              <div className="invalid-feedback">
                                 Please enter valid password.
                              </div>
                           </div>

                           <div className="mb-3">
                              <label htmlFor="password" className="form-label">
                                 Confirm New Password
                              </label>
                              <input
                                 type="password"
                                 id="password"
                                 className="form-control"
                                 name="password"
                                 placeholder="**************"
                                 required
                                 onChange={(e) =>
                                    setConfirmPassword(e.target.value)
                                 }
                              />
                              <div className="invalid-feedback">
                                 Please enter valid password.
                              </div>
                           </div>

                           <div>
                              <div className="d-grid">
                                 {isLoading ? (
                                    <button
                                       disabled
                                       type="button"
                                       className="btn btn-primary w-100 mb-4"
                                    >
                                       Processing{" "}
                                       <i className="fas fa-spinner fa-spin" />
                                    </button>
                                 ) : (
                                    <button
                                       type="submit"
                                       className="btn btn-primary w-100 mb-4"
                                    >
                                       Save Password{" "}
                                       <i className="fas fa-check-circle" />
                                    </button>
                                 )}
                              </div>
                           </div>
                        </form>
                     </div>
                  </div>
               </div>
            </div>
         </section>

         <BaseFooter />
      </>
   );
}

export default CreateNewPassword;
