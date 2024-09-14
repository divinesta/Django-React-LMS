const CartId = () => {
   const generateRandomString = () => {
      const length = 30;
      const characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
      let randomString = "";

      for (let i = 0; i < length; i++) {
         // const randomIndex = Math.floor(Math.random() * characters.length);
         // randomString += characters.charAt(randomIndex);
         randomString += characters.charAt(
            Math.floor(Math.random() * characters.length)
         );
      }

      localStorage.setItem("randomString", randomString);
   };

   let existingRandomString = localStorage.getItem("randomString");
   if (!existingRandomString) {
      generateRandomString();
      // return existingRandomString
   } else {
      // pass
      // return existingRandomString;
   }
   return existingRandomString;
};

export default CartId;
