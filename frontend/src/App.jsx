import { Route, Routes, BrowserRouter } from "react-router-dom";
import { useState, useEffect } from "react";
import MainWrapper from "./layout/MainWrapper";
import apiInstance from "./utils/axios";
import useAxios from "./utils/useAxios";
import CartId from "./views/plugin/CartId";
// import PrivateRoute from "./layout/PrivateRoute";
import { CartContext, ProfileContext } from "./views/plugin/Context";
import { userId } from "./utils/constants";
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";
import CreateNewPassword from "./views/auth/CreateNewPassword";

import Index from "./views/base/Index";
import CourseDetail from "./views/base/CourseDetail";
import Cart from "./views/base/Cart";
import Checkout from "./views/base/Checkout";
import Success from "./views/base/Success";
import Search from "./views/base/Search";

// Student Routes
import StudentDashboard from "./views/student/Dashboard";
import StudentCourses from "./views/student/Courses";
import StudentCourseDetail from "./views/student/CourseDetail";
import StudentChangePassword from "./views/student/ChangePassword";
import StudentWishlist from "./views/student/Wishlist";
import StudentProfile from "./views/student/Profile";

const App = () => {
   const cart_id = CartId();
   const [cartCount, setCartCount] = useState(0);
   const [profile, setProfile] = useState([]);

   useEffect(() => {
      apiInstance.get(`course/cart-list/${cart_id}/`).then((res) => {
         setCartCount(res.data?.length);


      useAxios().get(`user/profile/${userId}/`).then((res) => {
            // console.log(res.data);
            setProfile(res.data);
         });
      });
   }, []);

   return (
      <CartContext.Provider value={[cartCount, setCartCount]}>
         <ProfileContext.Provider  value={[profile, setProfile]}> 
            <BrowserRouter>
               <MainWrapper>
                  <Routes>
                     <Route path="/register/" element={<Register />} />
                     <Route path="/login/" element={<Login />} />
                     <Route path="/logout/" element={<Logout />} />
                     <Route path="/forgot-password/" element={<ForgotPassword />} />
                     <Route path="/create-new-password/" element={<CreateNewPassword />} />
                     {/* Base Routes */}
                     <Route path="/" element={<Index />} />
                     <Route path="/course-detail/:slug/" element={<CourseDetail />} />
                     <Route path="/cart/" element={<Cart />} />
                     <Route path="/checkout/:order_oid/" element={<Checkout />} />
                     <Route path="/payment-success/:order_oid/" element={<Success />} />
                     <Route path="/search/" element={<Search />} />
                     {/* Student Routes */}
                     <Route path="/student/dashboard/" element={<StudentDashboard />} />
                     <Route path="/student/change-password/" element={<StudentChangePassword />} />
                     <Route path="/student/courses/" element={<StudentCourses />} />
                     <Route path="/student/courses/:enrollment_id/" element={<StudentCourseDetail />} />
                     <Route path="/student/wishlist/" element={<StudentWishlist />} />
                     <Route path="/student/profile/" element={<StudentProfile />} />
                  </Routes>
               </MainWrapper>
            </BrowserRouter>
         </ProfileContext.Provider>
      </CartContext.Provider>
   );
};

export default App;
