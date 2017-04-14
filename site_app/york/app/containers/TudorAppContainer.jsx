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

import { connect } from "react-redux"

import * as reducers from "../reducers/index"

import Courses from "../components/Courses"
import Course from "../components/Course"
import TopBarMenu from "../components/TopBarMenu"
import Profile from "../components/Profile"
import AuthHelper from "../components/AuthHelper"
import * as actions from "../actions/mainActions"

import * as axios from "axios"

const isAuth = {
    isAuthenticated: !!localStorage.token,
    signout(cb) {
        delete localStorage.token;
    }
}

class Login extends React.Component {
    constructor(props) {
        super(props);
        if (localStorage.token) {
            this.state = { isAuthenticated: true };
        } else {
            this.state = { isAuthenticated: false };
        }
        this.handleUsernameChange = this.handleUsernameChange.bind(this);
        this.handlePasswordChange = this.handlePasswordChange.bind(this);
    }

    getToken = (username, pass, cb) => {
        axios.post('/api/obtain-auth-token/', {
            username: this.state.username,
            password: this.state.password
        }).then((response) => {
            console.log(response);
            cb({ authenticated: true, token: response.data.token })
        }).catch((error) => {
            cb({ authenticated: false, error: "Incorrect Credentials"})
        })
    }

    login = (e) => {
        e.preventDefault();
        const password = this.state.password;
        const username = this.state.username;
        this.getToken(username, password, (res) => {
            if (res.authenticated) {
                console.log(res);
                localStorage.setItem('token',res.token);
                this.setState({isAuthenticated: true});
            } else {
                alert(res.error);
            }
        })
    }

    logout = () =>{
        delete localStorage.token;
        this.setState({isAuthenticated: false});
    }

    handleUsernameChange(event) {
        this.setState({username: event.target.value});
    }

    handlePasswordChange(event) {
        this.setState({password: event.target.value});
    }

    render() {
        const isAuthenticated = this.state.isAuthenticated;
        return isAuthenticated ? <button onClick={this.logout}>Logout</button>  : (
            <form onSubmit={this.login}>
                <input type="text" name="username" placeholder="Username" onChange={this.handleUsernameChange}/>
                <input type="password" name="password" placeholder="Password" onChange={this.handlePasswordChange}/>
                <input type="submit"/>
            </form>)
    }
}

@connect(state => ({state}))
export default class TudorAppContainer extends React.Component {
   constructor(props) {
     super(props);
   }

    render() {
        const {isLoadingState} = this.props.state.main;
        return (
            <Router>
                <div>
                    <AuthHelper/>
                    <TopBarMenu/>
                    { isLoadingState ? <div className="tudor-global__loading_state"></div> : null }
                    <div className="app-content">
                        <Route exact path="/" component={AuthHelper}/>
                        <Route path="/login" component={Login}/>
                        <Route path="/courses" component={Courses}/>
                        <Route path="/course/:id" component={Course}/>
                        <Route path="/profile" component={Profile}/>
                    </div>
                </div>
            </Router>
        )
    }
}
