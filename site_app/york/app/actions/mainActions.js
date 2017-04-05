export const SET_COURSES = "SET_COURSES";
export const SET_GLOBAL_HEADER_TOKEN = "SET_GLOBAL_HEADER_TOKEN";
export const CLOSE_RENAME_POPUP = "CLOSE_RENAME_POPUP";
export const OPEN_RENAME_POPUP = "OPEN_RENAME_POPUP";

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

// export function setRename() {
//     return {type: "RENAME"}
// }
