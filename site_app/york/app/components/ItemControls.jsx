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

import { Classes, Menu, MenuDivider, MenuItem } from "@blueprintjs/core";

@connect(state => ({state}))
export default class ItemControls extends React.Component {
    constructor(props) {
        super(props);
        this.state = {item: props.item};

        this.stateOfSelected = this.stateOfSelected.bind(this);
        this.controlsOfSelected = this.controlsOfSelected.bind(this);
    }

    componentDidMount() {
    }

    componentWillReceiveProps(nextProps) {
        if(JSON.stringify(this.props.item) !== JSON.stringify(nextProps.item)) {
           this.setState({item: nextProps.item});
        }
    }

    stateOfSelected() {
        if (this.state.item) {
            return (
                <div className="pt-callout pt-intent-success tudor-item-controls__msg pt-icon-info-sign">
                    <h5>Selected object: {this.state.item.label}</h5>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ex, delectus!
                </div>
            )
        } else {
            return (
                <div className="pt-callout pt-intent-primary tudor-item-controls__msg pt-icon-info-sign">
                    <h5>Selected object:</h5>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ex, delectus!
                </div>
            )
        }
    }

    controlsOfSelected() {
        return (
            <div className="tudor-item-controls__controls">
                <Menu className={`docs-inline-example ${Classes.ELEVATION_1}`}>
                    <MenuItem iconName="new-text-box" text="New text box" />
                    <MenuItem iconName="new-object" text="New object" />
                    <MenuItem iconName="new-link" text="New link" />
                    <MenuDivider />
                    <MenuItem
                        iconName="cog"
                        label={<span className="pt-icon-standard pt-icon-share" />}
                        text="Settings..."
                    />
                </Menu>
            </div>
        )
    }

    render() {
        return (
            <div>
                <div className="tudor-item-controls">
                    {this.controlsOfSelected()}
                    {this.stateOfSelected()}
                </div>
            </div>
        )
    }

}
