export const SET_COURSES = "SET_COURSES";
export const SET_GLOBAL_HEADER_TOKEN = "SET_GLOBAL_HEADER_TOKEN";

export function setGlobalHeaderToken(token) {
    return {type: SET_GLOBAL_HEADER_TOKEN, token}
}

export function setCourses(courses) {
    return {type: SET_COURSES, courses}
}
