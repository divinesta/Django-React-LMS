import { Route, Routes, BrowserRouter } from "react-router-dom";

import MainWrapper from "./layout/MainWrapper";
// import PrivateRoute from "./layout/PrivateRoute";
import Dashboard from './views/auth/Dashboard'
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";
import Logout from "./views/auth/Logout"

const App = () => {
   return (
      <BrowserRouter>
         <MainWrapper>
            <Routes>
               <Route path="/" element={<Dashboard />} />
               <Route path="/register/" element={<Register />} />
               <Route path="/login/" element={<Login />} />
               <Route path="/logout/" element={<Logout />} />
            </Routes>
         </MainWrapper>
      </BrowserRouter>
   );
}

export default App;
