import React, {PropTypes} from 'react'
import {render} from 'react-dom'
import * as _ from 'lodash';
import {
    BrowserRouter as Router,
    Route,
    Link,
    Redirect,
    withRouter
} from 'react-router-dom'
import createHistory from 'history/createBrowserHistory'
const history = createHistory();

import {
  createStore,
  compose,
  applyMiddleware,
  combineReducers,
} from "redux"
import { Provider, connect } from "react-redux"
import thunk from "redux-thunk"

import * as reducers from "./reducers/index"
import TudorAppContainer from "./containers/TudorAppContainer"


let finalCreateStore = compose(
  applyMiddleware(thunk),
  window.devToolsExtension ? window.devToolsExtension() : f => f
)(createStore);
let reducer = combineReducers(reducers);
let store = finalCreateStore(reducer);


const AuthExample = () => (
    <Provider store={store}>
        <TudorAppContainer/>
    </Provider>
)

render(<AuthExample/>, document.getElementById('TudorApp'));

