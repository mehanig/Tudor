export const SET_IS_LOADING_TRUE = "SET_IS_LOADING_TRUE";
export const SET_IS_LOADING_FALSE = "SET_IS_LOADING_FALSE";
export const SET_COURSES = "SET_COURSES";
export const SET_GLOBAL_HEADER_TOKEN = "SET_GLOBAL_HEADER_TOKEN";
export const CLOSE_RENAME_POPUP = "CLOSE_RENAME_POPUP";
export const OPEN_RENAME_POPUP = "OPEN_RENAME_POPUP";
export const SET_COURSE_STRUCTURE = "SET_COURSE_STRUCTURE";

export function setIsLoadingFalse() {
   return {type: SET_IS_LOADING_FALSE}
}

export function setIsLoadingTrue() {
   return {type: SET_IS_LOADING_TRUE}
}

export function setGlobalHeaderToken(token) {
    return {type: SET_GLOBAL_HEADER_TOKEN, token}
}

export function setCourses(courses) {
    return {type: SET_COURSES, courses}
}

export function setRenamePopupClosed() {
    return {type: CLOSE_RENAME_POPUP}
}

export function setRenamePopupOpen() {
    return {type: OPEN_RENAME_POPUP}
}

export function setCourseStructure(course_id, course_data) {
    return {type: "SET_COURSE_STRUCTURE",course_id, course_data}
}
// export function setRename() {
//     return {type: "RENAME"}
// }
