import { useState, useEffect } from "react";




const GetCurrentAddress = () => {
   const [address, setAddress] = useState(null);
   if (!navigator.geolocation) {
      console.error("Geolocation is not supported by your browser");
   } else {
      console.log("Locating...");
   }


   useEffect(() => {
      navigator.geolocation.getCurrentPosition((position) => {
         const { latitude, longitude } = position.coords;

         const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`;
         
         fetch(url)
            .then((response) => response.json())
            .then((data) => setAddress(data.address));
      });
   }, []);

   return address;
};

export default GetCurrentAddress;
