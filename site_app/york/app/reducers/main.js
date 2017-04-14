import * as Actions from "../actions/mainActions"

const initialState = {
    courses: [],
    globalHeaderToken: false,
    renamePopup: false,
    isLoadingState: false,
};

export default function submissions(state = initialState, action = {}) {
    switch (action.type) {
        case Actions.SET_IS_LOADING_TRUE:
            return {...state, isLoadingState: true};
        case Actions.SET_IS_LOADING_FALSE:
            return {...state, isLoadingState: false};
        case Actions.SET_COURSES:
            return {...state, courses: action.courses};
        case Actions.SET_GLOBAL_HEADER_TOKEN:
            return {...state, globalHeaderToken: action.token};
        case Actions.CLOSE_RENAME_POPUP:
            return {...state, renamePopup: false};
        case Actions.OPEN_RENAME_POPUP:
            return {...state, renamePopup: true};
        case Actions.SET_COURSE_STRUCTURE:
            const new_state = state;
            new_state.courses[action.course_id] = action.course_data;
            return {...new_state};
        default:
            return state
    }
}
