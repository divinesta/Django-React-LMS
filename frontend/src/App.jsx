import { Route, Routes, BrowserRouter } from "react-router-dom";

import MainWrapper from "./layout/MainWrapper";
// import PrivateRoute from "./layout/PrivateRoute";
import Dashboard from './views/auth/Dashboard'
import Register from "./views/auth/Register";
import Login from "./views/auth/Login";

function App() {
   return (
      <BrowserRouter>
         <MainWrapper>
            <Routes>
               <Route path="/" element={<Dashboard />} />
               <Route path="/register/" element={<Register />} />
               <Route path="/login/" element={<Login />} />
            </Routes>
         </MainWrapper>
      </BrowserRouter>
   );
}

export default App;
