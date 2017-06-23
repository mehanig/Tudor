import * as Actions from "../actions/mainActions"

const initialState = {
    courses: [],
    globalHeaderToken: false,
    renamePopup: false,
    isLoadingState: false,
    addLessonPopup: false,
    addStepPopup: false,
    addSubStepPopup: false,
    deleteItemPopup: false
};

export default function submissions(state = initialState, action = {}) {
    switch (action.type) {
        case Actions.SET_IS_LOADING_TRUE:
            return {...state, isLoadingState: true}
        case Actions.SET_IS_LOADING_FALSE:
            return {...state, isLoadingState: false}
        case Actions.SET_COURSES:
            return {...state, courses: action.courses}
        case Actions.SET_GLOBAL_HEADER_TOKEN:
            return {...state, globalHeaderToken: action.token}
        case Actions.CLOSE_RENAME_POPUP:
            return {...state, renamePopup: false}
        case Actions.OPEN_RENAME_POPUP:
            return {...state, renamePopup: true}
        case Actions.OPEN_ADDLESSON_POPUP:
            return {...state, addLessonPopup: true}
        case Actions.OPEN_ADDSTEP_POPUP:
            return {...state, addStepPopup: true}
        case Actions.OPEN_ADDSUBSTEP_POPUP:
            return {...state, addSubStepPopup: true}
        case Actions.CLOSE_ADDITEM_POPUP:
            const flag = action.flag;
            return {...state, [flag]: false}
        case Actions.OPEN_DELETEITEM_POPUP:
            return {...state, deleteItemPopup: true}
        case Actions.CLOSE_DELETEITEM_POPUP:
            return {...state, deleteItemPopup: false}
        case Actions.SET_COURSE_STRUCTURE:
            let id = state.courses.findIndex((el) => el.key == action.course_id)
            state.courses[id] = action.course_data
            return {...state}
        default:
            return state
    }
}
