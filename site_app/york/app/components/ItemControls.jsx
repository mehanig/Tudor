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
export default class ItemControls extends React.Component {
    constructor(props) {
        super(props);
        this.state = {item: props.item,
                      showRename: false,
                      showDelete: false};

        this.stateOfSelected = this.stateOfSelected.bind(this);
        this.controlsOfSelected = this.controlsOfSelected.bind(this);
        this.handleDelete =  this.handleDelete.bind(this);
        this.handleRename = this.handleRename.bind(this);
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
                    {this.state.item.label} at {this.state.item.local_path}
                </div>
            )
        } else {
            return (
                <div className="pt-callout pt-intent-primary tudor-item-controls__msg pt-icon-info-sign">
                    <h5>No object selected</h5>
                    <br/>
                </div>
            )
        }
    }

    handleRename() {
        let {dispatch} = this.props;
        if (this.state.item) {
            dispatch(actions.setRenamePopupOpen());
        }
    }

    handleDelete() {
        let {dispatch} = this.props;
        if (this.state.item) {
            // this.setState({...this.state, showDelete: true});
        }
    }

    controlsOfSelected() {
        return (
            <div className="tudor-item-controls__controls">
                <Menu className={`docs-inline-example ${Classes.ELEVATION_1}`}>
                    <RenamePopup item={this.state.item} course_id={this.props.course_id}/>
                    <MenuItem iconName="edit" text="Rename" onClick={this.handleRename}/>
                    <MenuItem iconName="trash" text="Delete" onClick={this.handleDelete} />
                    <MenuDivider />
                    <MenuItem
                        iconName="cog"
                        label={<span className="pt-icon-annotation pt-icon-share" />}
                        text="Notes2..."
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
