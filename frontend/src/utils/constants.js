import UserData from "../views/plugin/UserData"

const user_id = UserData()?.user_id;
// console.log("User ID:", user_id);
const teacher_id = UserData()?.teacher_id


export const API_BASE_URL = "http://127.0.0.1:8000/api/v1/";
export const userId = user_id;
export const teacherId = teacher_id