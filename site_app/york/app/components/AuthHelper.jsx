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

import * as actions from "../actions/mainActions"
import * as axios from "axios"

@connect(state => ({state}))
export default class AuthHelper extends React.Component {
    constructor(props) {
        super(props);
        this.state = { data: null }
    }

    componentDidMount() {
        let {dispatch} = this.props;
        if (localStorage.token) {
            dispatch(actions.setGlobalHeaderToken(localStorage.token));
            axios.get('/api/users/i/', {'headers':{'Authorization': 'Token ' + localStorage.token}}).then(function (data) {
                this.setState({data: data.data});
            }.bind(this)).catch(() => {
                this.setState({data: {error: true}});
            });
        } else {
            this.setState({data: {error: true}});
        }

    }

    render() {
        if (_.has(this.state, ['data', 'username'])) {
                return <Redirect to={{
                    pathname: '/courses',
                    state: {from: '/'}
                }}/>
        } else if (_.has(this.state, ['data', 'error'])) {
                return <Redirect to={{
                    pathname: '/login',
                    state: {from: '/'}
                }}/>
        } else {
            return <div>Loading...</div>;
        }
    }
}
