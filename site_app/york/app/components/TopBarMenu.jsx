import React from "react"
import {connect} from "react-redux"
import * as counterActions from "../actions/mainActions"
import * as axios from "axios"

import { Navbar} from "@blueprintjs/core";
import {
    Route,
    Link,
    Redirect,
    withRouter
} from 'react-router-dom'

@connect(state => ({state}))
export default class TopBarMenu extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            feed: []
        }
    }

    componentWillMount() {
        let {dispatch, counters} = this.props;
    }


    render() {
        let {counters} = this.props;

        return (
            <nav className="pt-navbar pt-dark">
                <div className="pt-navbar-group pt-align-left">
                    <div className="pt-navbar-heading">TudorStudio</div>
                    <input className="pt-input" placeholder="Search files..." type="text"/>
                </div>
                <div className="pt-navbar-group pt-align-right">
                    <Link to="/"><button className="pt-button pt-minimal pt-icon-home">Home</button></Link>
                    <button className="pt-button pt-minimal pt-icon-document">Files</button>
                    <span className="pt-navbar-divider"></span>
                    <Link to="/profile"><button className="pt-button pt-minimal pt-icon-user"></button></Link>
                    <button className="pt-button pt-minimal pt-icon-notifications"></button>
                    <Link to="/settings"><button className="pt-button pt-minimal pt-icon-cog"></button></Link>
                </div>
            </nav>
        )
    }
}
