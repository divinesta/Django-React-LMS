import { useEffect, useState } from "react";
import { setUser } from "../utils/auth";

const MainWrapper = ({ children }) => {
   const [loading, setLoading] = useState(true);

   useEffect(() => {
      const handler = async () => {
         setLoading(true);
         try {
            await setUser();
         } catch (error) {
            console.error("Failed to set user:", error);
         }
         setLoading(false);
      };
      handler();
   }, []);

   return (
      <>
         {loading ? (
            <div>Loading...</div> // Add a loading indicator
         ) : (
            children
         )}
      </>
   );
};

export default MainWrapper;
