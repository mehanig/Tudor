import * as classNames from "classnames"
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

import {
    Button,
    Classes,
    IBackdropProps,
    Intent,
    IOverlayableProps,
    Overlay,
    Switch,
} from "@blueprintjs/core";

const OVERLAY_CLASS = "docs-overlay-example-transition";


@connect(state => ({state}))
export default class RenamePopup extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            "new_name": "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleRename = this.handleRename.bind(this);
        this.handleTextInputChange = this.handleTextInputChange.bind(this);
    }

    componentDidMount() {
    }

    handleClose() {
        let {dispatch} = this.props;
        dispatch(actions.setAddItemPopupClose(this.props.isOpenFlagState));
    }

    //TODO rewrite to make async actions
    handleRename() {
        let {dispatch} = this.props;
        // dispatch(actions.setRename());
        const token = this.props.state.main.globalHeaderToken;
        const { course_id } = this.props;
        const data = {
            "action": "add",
            "new_path": this.props.item.local_path + "/" + this.state.new_name,
            "new_name": this.state.new_name
        };
        dispatch(actions.setIsLoadingTrue());
        alert(data.new_path)
        dispatch(actions.setIsLoadingFalse());
    }

    handleTextInputChange(e) {
        console.log(e.target.value);
        this.setState({new_name: e.target.value});
    }

    render() {
        const classes = "pt-card pt-elevation-4 docs-overlay-example-transition pt-overlay-content tudor-popup";
        const selected = this.props.item;
        return (
            <div>
                { selected ?
                    <Overlay onClose={this.handleClose} isOpen={this.props.state.main[this.props.isOpenFlagState]}>
                        <div className={classes} >
                            <h3>Create Object</h3>
                            <p>
                                Enter new name for object:
                            </p>
                            <p>
                                <input className="pt-input pt-intent-primary" type="text" placeholder={selected.name} dir="auto" onChange={this.handleTextInputChange}/>
                            </p>
                            <br />
                            <Button intent={Intent.DANGER} onClick={this.handleClose}>Close</Button>
                            <Button onClick={this.handleRename} style={{ float: "right" }}>Rename</Button>
                        </div>
                    </Overlay>
                    :
                    <div></div>
                }
            </div>
        );
    }

}