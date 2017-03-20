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


import * as axios from "axios"

const AuthExample = () => (
    <Router>
        <div>
            <UserMenu/>
            <ul>
                <li><Link to="/app">Settings Page</Link></li>
                <li><Link to="/protected">Protected Page</Link></li>
            </ul>
            <Route path="/app" component={Public}/>
            <Route path="/login" component={Login}/>
            <PrivateRoute path="/app2" component={Protected}/>
        </div>
    </Router>
)

const fakeAuth = {
    isAuthenticated: false,
    authenticate(cb) {
        this.isAuthenticated = true
        setTimeout(cb, 100) // fake async
    },
    signout(cb) {
        this.isAuthenticated = false
        setTimeout(cb, 100)
    }
}

const AuthButton = withRouter(({history}) => {
    // return axios.get('api/users/i/').then((resp)=>{
    //     if (resp.data.username) {
    //         return <p>Welcome!</p>
    //     } else {
    //         return <p>Log in</p>
    //     }
    // });
    return fakeAuth.isAuthenticated ? (
            <p>
                Welcome!
                <button onClick={() => {
                    fakeAuth.signout(() => history.push('/'))
                }}>Sign out
                </button>
            </p>
        ) : (
            <p>You are not logged in.</p>
        )
})

const UserMenu = React.createClass({
    getInitialState: function () {
        return {data: null};
    },

    componentDidMount: function () {
        axios.get('api/users/i/').then(function (data) {
            this.setState({data: data.data});
        }.bind(this));
    },

    render: function () {
        console.log(this.state);
        if (_.has(this.state, ['data', 'username'])) {
            if (this.state.data.username) {
                return <Redirect to={{
                    pathname: '/app',
                    state: {from: '/'}
                }}/>
            } else {
                return <Redirect to={{
                    pathname: '/login',
                    state: {from: '/'}
                }}/>
            }
        } else {
            return <div>Loading...</div>;
        }
    }
});

const PrivateRoute = ({component, ...rest}) => (
    <Route {...rest} render={props => (
        fakeAuth.isAuthenticated ? (
                React.createElement(component, props)
            ) : (
                <Redirect to={{
                    pathname: '/login',
                    state: {from: props.location}
                }}/>
            )
    )}/>
)

const Public = () => <h3>Public</h3>
const Protected = () => <h3>Protected</h3>

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
            cb({ authenticated: true, token: response.token })
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
                localStorage.token = res.token;
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
        return isAuthenticated ? <button onClick={this.logout}>Logout</button> : (
            <form onSubmit={this.login}>
                <input type="text" name="username" placeholder="Username" onChange={this.handleUsernameChange}/>
                <input type="password" name="password" placeholder="Password" onChange={this.handlePasswordChange}/>
                <input type="submit"/>
            </form>)
    }
}


//
render(<AuthExample/>, document.getElementById('TudorApp'));

