import { useState, useEffect } from "react";
import moment from "moment";

import Sidebar from "./Partials/Sidebar";
import Header from "./Partials/Header";
import BaseHeader from "../partials/BaseHeader";
import BaseFooter from "../partials/BaseFooter";

import useAxios from "../../utils/useAxios";
import { teacherId } from "../../utils/constants";
import Toast from "../plugin/Toast";

const TeacherNotification = () => {
   const [notification, setNotification] = useState([]);

   const fetchNotification = () => {
      useAxios()
         .get(`teacher/noti-list/${teacherId}/`)
         .then((res) => {
            setNotification(res.data);
            console.log(res.data);
         });
   };

   useEffect(() => {
      fetchNotification();
   }, []);

   const handleMarkAsSeen = (notiId) => {
      const formdata = new FormData();

      formdata.append("teacher", teacherId);
      formdata.append("pk", notiId);
      formdata.append("seen", true);

      useAxios()
         .patch(`teacher/noti-detail/${teacherId}/${notiId}/`, formdata)
         .then((res) => {
            console.log(res.data);
            fetchNotification();
            Toast.fire({
               icon: "success",
               title: "Notication Seen",
            });
         });
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
                     {/* Card */}
                     <div className="card mb-4">
                        {/* Card header */}
                        <div className="card-header d-lg-flex align-items-center justify-content-between">
                           <div className="mb-3 mb-lg-0">
                              <h3 className="mb-0">Notifications</h3>
                              <span>Manage all your notifications from here</span>
                           </div>
                        </div>
                        {/* Card body */}
                        <div className="card-body">
                           {/* List group */}
                           <ul className="list-group list-group-flush">
                              {/* List group item */}
                              {notification?.map((n, index) => (
                                 <li className="list-group-item p-4 shadow rounded-3 mb-3" key={index}>
                                    <div className="d-flex">
                                       <div className="ms-3 mt-2">
                                          <div className="d-flex align-items-center justify-content-between">
                                             <div>
                                                <h4 className="mb-0">{n.type}</h4>
                                             </div>
                                          </div>
                                          <div className="mt-2">
                                             <p className="mt-1">
                                                <span className="me-2 fw-bold">
                                                   Date: <span className="fw-light">{moment(n.date).format("DD MMM, YYYY")}</span>
                                                </span>
                                             </p>
                                             <p>
                                                <button class="btn btn-outline-secondary" type="button" onClick={() => handleMarkAsSeen(n.id)}>
                                                   Mark as Seen <i className="fas fa-check"></i>
                                                </button>
                                             </p>
                                          </div>
                                       </div>
                                    </div>
                                 </li>
                              ))}

                              {notification?.length < 1 && <p>No notifications</p>}
                           </ul>
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

export default TeacherNotification;
