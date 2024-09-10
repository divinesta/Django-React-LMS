import { useState } from "react";
import apiInstance from "../../utils/axios";
import { useNavigate, Link } from "react-router-dom";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import Swal from "sweetalert2";

const Toast = Swal.mixin({
   toast: true,
   position: "top",
   showConfirmButton: false,
   timer: 3000,
   timerProgressBar: true,
});


const ForgotPassword = () => {

      const [email, setEmail] = useState("")
   const [isLoading, setIsLoading] = useState(false)
   const navigate = useNavigate()

   const handleSubmit = async (e) => {
      e.preventDefault()
      setIsLoading(true)
      try {
         await apiInstance.get(`user/password-reset/${email}/`).then((res) => {
            console.log(res.data);
            
            setIsLoading(false)
            Toast.fire({
               icon: "info",
               title: "An Email has been sent to you"
            })
      })
      } catch (error) {
         // console.log(error)
         setIsLoading(false)
      }
   }

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
                           <h1 className="mb-1 fw-bold">Forgot Password</h1>
                           <span>
                              Let's help you get back into your account
                           </span>
                        </div>
                        <form
                           className="needs-validation"
                           noValidate=""
                           onSubmit={handleSubmit}
                        >
                           <div className="mb-3">
                              <label htmlFor="email" className="form-label">
                                 Email Address
                              </label>
                              <input
                                 type="email"
                                 id="email"
                                 className="form-control"
                                 name="email"
                                 placeholder="Enter your email here..."
                                 required
                                 onChange={(e) => setEmail(e.target.value)}
                              />
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
                                       <i className="fas fa-spinner fa-spin"></i>
                                    </button>
                                 ) : (
                                    <button
                                       type="submit"
                                       className="btn btn-primary w-100 mb-4"
                                    >
                                       Send Email{" "}
                                       <i className="fas fa-paper-plane"></i>
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

export default ForgotPassword;
