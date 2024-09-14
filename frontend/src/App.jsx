import { Route, Routes, BrowserRouter } from "react-router-dom";

import MainWrapper from "./layout/MainWrapper";
// import PrivateRoute from "./layout/PrivateRoute";
import Dashboard from './views/auth/Dashboard'
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout"
import ForgotPassword from "./views/auth/ForgotPassword"
import CreateNewPassword from "./views/auth/CreateNewPassword"

import Index from "./views/base/Index";
import CourseDetail from "./views/base/CourseDetail";
import Cart from "./views/base/Cart";


const App = () => {
   return (
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
            </Routes>
         </MainWrapper>
      </BrowserRouter>
   );
}

export default App;
