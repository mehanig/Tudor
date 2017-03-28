import * as Actions from "../actions/mainActions"

const initialState = {
    courses: [],
    globalHeaderToken: false
};

export default function submissions(state = initialState, action = {}) {
    switch (action.type) {
        case Actions.SET_COURSES:
            console.log("settingHERE");
            console.log(action.courses);
            return {...state, courses: action.courses};
        case Actions.SET_GLOBAL_HEADER_TOKEN:
            return {...state, globalHeaderToken: action.token};
        default:
            return state
    }
}
