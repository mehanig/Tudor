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
            "new_name": ""
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleRename = this.handleRename.bind(this);
        this.handleTextInputChange = this.handleTextInputChange.bind(this);
    }

    componentDidMount() {
    }

    handleClose() {
        let {dispatch} = this.props;
        dispatch(actions.setRenamePopupClosed());
    }

    //TODO rewrite to make async actions
    handleRename() {
        let {dispatch} = this.props;
        // dispatch(actions.setRename());
        const token = this.props.state.main.globalHeaderToken;
        const { course_id } = this.props;
        const data = {
            "action": "rename",
            "old_path": this.props.item.local_path,
            "new_name": this.state.new_name
        };
        dispatch(actions.setIsLoadingTrue());
        axios.put(`/api/courses/${course_id}/`, data, {'headers':{'Authorization': 'Token ' + localStorage.token}}).then((res)=> {
            this.handleClose();
            axios.get(`/api/courses/${course_id}/`, {'headers':{'Authorization': 'Token ' + localStorage.token}}).then((res) => {
                console.log("___");
                console.log(res);
                const course_data = res.data;
                dispatch(actions.setCourseStructure(course_id, course_data));
                setTimeout( () => {dispatch(actions.setIsLoadingFalse())}, 2000);
            }).catch((res) => {
                console.log(res);
                alert("Error fetching course data")
            });
        }).catch((res)=> {
            console.log(res.data);
        });
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
                    <Overlay onClose={this.handleClose} isOpen={this.props.state.main.renamePopup}>
                        <div className={classes} >
                            <h3>Rename Object</h3>
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
