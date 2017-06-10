import React, {PropTypes} from 'react'
import {render} from 'react-dom'
import {connect} from "react-redux"
import {
    Route,
    Link,
    Redirect,
    withRouter
} from 'react-router-dom'

import * as axios from "axios"
import * as actions from "../actions/mainActions"

import RenamePopup from "../components/RenamePopup";

import { Classes, Menu, MenuDivider, MenuItem } from "@blueprintjs/core";

@connect(state => ({state}))
export default class RecorderControls extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <div className="tudor-recorder-controls">
                    <span>Start Recording</span>
                    <span></span>
                </div>
            </div>
        )
    }

}
