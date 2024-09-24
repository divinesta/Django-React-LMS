import { useState, useEffect, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";
import Sidebar from "./Partials/Sidebar";
import Header from "./Partials/Header";
import Rater from "react-rater";
import "react-rater/lib/react-rater.css";
import CartId from "../plugin/CartId";
import GetCurrentAddress from "../plugin/UserCountry";
import useAxios from "../../utils/useAxios";
import { userId } from "../../utils/constants";
import Toast from "../plugin/Toast";
import { CartContext } from "../plugin/Context";



const Wishlist = () => {
   const [wishlists, setWishlist] = useState([]);
   const [cartCount, setCartCount] = useContext(CartContext);

   const cart_id = CartId();
   const country = GetCurrentAddress();
   // console.log(country);

   const fetchWishist = () => {
      useAxios()
         .get(`student/wishlist/${userId}/`)
         .then((res) => {
            setWishlist(res.data);
            console.log(res.data);
         });
   };

   useEffect(() => {
      fetchWishist();
   }, []);

   const addToCart = async (courseId, userId, price, country, cartId) => {
      const formdata = new FormData();

      formdata.append("course_id", courseId);
      formdata.append("user_id", userId);
      formdata.append("price", price);
      formdata.append("country_name", country);
      formdata.append("cart_id", cartId);

      try {
         await useAxios()
            .post(`course/cart/`, formdata)
            .then((res) => {
               console.log(res.data);
               Toast.fire({
                  title: "Added To Cart",
                  icon: "success",
               });

               // Set cart count after adding to cart
               useAxios()
                  .get(`course/cart-list/${CartId}/`)
                  .then((res) => {
                     setCartCount(res.data?.length);
                  });
            });
      } catch (error) {
         console.log(error);
      }
   };

   return (
      <>
         <BaseHeader />

         <section className="pt-5 pb-5">
            <div className="container">
               {/* Header Here */}
               <Header />
               <div className="row mt-0 mt-md-4">
                  {/* Sidebar Here */}
                  <Sidebar />
                  <div className="col-lg-9 col-md-8 col-12">
                     <h4 className="mb-0 mb-4">
                        {" "}
                        <i className="fas fa-heart"></i> Wishlist{" "}
                     </h4>

                     <div className="row">
                        <div className="col-md-12">
                           <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
                              {wishlists?.map((wishlist, index) => (
                                 <div className="col-lg-4" key={index}>
                                    {/* Card */}
                                    <div className="card card-hover">
                                       <Link to={`/course-detail/${wishlist.course.slug}/`}>
                                          <img
                                             src={wishlist.course?.image}
                                             alt="course"
                                             className="card-img-top"
                                             style={{
                                                width: "100%",
                                                height: "200px",
                                                objectFit: "cover",
                                             }}
                                          />
                                       </Link>
                                       {/* Card Body */}
                                       <div className="card-body">
                                          <div className="d-flex justify-content-between align-items-center mb-3">
                                             <div>
                                                <span className="badge bg-info">{wishlist.course?.level}</span>
                                                <span className="badge bg-info ms-2">{wishlist.course?.language}</span>
                                             </div>
                                             <a href="#" className="fs-5">
                                                <i className="fas fa-heart text-danger align-middle" />
                                             </a>
                                          </div>
                                          <h4 className="mb-2 text-truncate-line-2 ">
                                             <Link to={`/course-detail/${wishlist.course.slug}/`} className="text-inherit text-decoration-none text-dark fs-5">
                                                {wishlist.course?.title}
                                             </Link>
                                          </h4>
                                          <small>By: {wishlist.course.teacher.full_name}</small> <br />
                                          <small>
                                             {wishlist.course.students?.length} Student
                                             {wishlist.course.students?.length > 1 && "s"}
                                          </small>{" "}
                                          <br />
                                          <div className="lh-1 mt-3 d-flex">
                                             <span className="align-text-top">
                                                <span className="fs-6">
                                                   <Rater total={5} rating={wishlist.course.average_rating || 0} />
                                                </span>
                                             </span>
                                             <span className="text-warning">4.5</span>
                                             <span className="fs-6 ms-2">({wishlist.course.reviews?.length} Reviews)</span>
                                          </div>
                                       </div>
                                       {/* Card Footer */}
                                       <div className="card-footer">
                                          <div className="row align-items-center g-0">
                                             <div className="col">
                                                <h5 className="mb-0">${wishlist.course.price}</h5>
                                             </div>
                                             <div className="col-auto">
                                                <button
                                                   onClick={() => addToCart(wishlist.course.id, userId, wishlist.course.price, country?.country, cart_id)}
                                                   type="button"
                                                   className="text-inherit text-decoration-none btn btn-primary me-2"
                                                >
                                                   <i className="fas fa-shopping-cart text-primary text-white" />
                                                </button>
                                                <Link to={""} className="text-inherit text-decoration-none btn btn-primary">
                                                   Enroll Now <i className="fas fa-arrow-right text-primary align-middle me-2 text-white" />
                                                </Link>
                                             </div>
                                          </div>
                                       </div>
                                    </div>
                                 </div>
                              ))}
                           </div>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
         </section>

         <BaseFooter />
      </>
   );
};

export default Wishlist;
