import { Route, Routes, BrowserRouter } from "react-router-dom";
import { useState, useEffect } from "react";
import MainWrapper from "./layout/MainWrapper";
import apiInstance from "./utils/axios";
import CartId from "./views/plugin/CartId";
// import PrivateRoute from "./layout/PrivateRoute";
import { CartContext } from "./views/plugin/Context";
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout";
import ForgotPassword from "./views/auth/ForgotPassword";
import CreateNewPassword from "./views/auth/CreateNewPassword";

import Index from "./views/base/Index";
import CourseDetail from "./views/base/CourseDetail";
import Cart from "./views/base/Cart";
import Checkout from "./views/base/Checkout"
import Success from "./views/base/Success";

const App = () => {
   const cart_id = CartId();
   const [cartCount, setCartCount] = useState(0);

   useEffect(() => {
      apiInstance.get(`course/cart-list/${cart_id}/`).then((res) => {
         setCartCount(res.data?.length);
      });
   }, []);

   return (
      <CartContext.Provider value={[cartCount, setCartCount]}>
         <BrowserRouter>
            <MainWrapper>
               <Routes>
                  <Route path="/register/" element={<Register />} />
                  <Route path="/login/" element={<Login />} />
                  <Route path="/logout/" element={<Logout />} />
                  <Route
                     path="/forgot-password/"
                     element={<ForgotPassword />}
                  />
                  <Route
                     path="/create-new-password/"
                     element={<CreateNewPassword />}
                  />
                  {/* Base Routes */}
                  <Route path="/" element={<Index />} />
                  <Route
                     path="/course-detail/:slug/"
                     element={<CourseDetail />}
                  />
                  <Route path="/cart/" element={<Cart />} />
                  <Route path="/checkout/:order_oid/" element={<Checkout />} />
                  <Route path="/payment-success/:order_oid/" element={<Success />} />
               </Routes>
            </MainWrapper>
         </BrowserRouter>
      </CartContext.Provider>
   );
};

export default App;
