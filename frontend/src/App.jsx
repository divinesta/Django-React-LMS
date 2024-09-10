import { Route, Routes, BrowserRouter } from "react-router-dom";

import MainWrapper from "./layout/MainWrapper";
// import PrivateRoute from "./layout/PrivateRoute";

import Register from "../src/views/auth/Register";

function App() {
   return (
      <BrowserRouter>
         <MainWrapper>
            <Routes>
               <Route path="/register" element={<Register />} />
            </Routes>
         </MainWrapper>
      </BrowserRouter>
   );
}

export default App;
