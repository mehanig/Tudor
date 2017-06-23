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
            "path": "",
        };
        this.handleClose = this.handleClose.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
    }

    componentDidMount() {
    }

    handleClose() {
        let {dispatch} = this.props;
        dispatch(actions.setCloseDeleteItemPopup());
    }

    //TODO rewrite to make async actions
    handleDelete() {
        let {dispatch} = this.props;
        const token = this.props.state.main.globalHeaderToken;
        const { course_id } = this.props;
        const data = {
            "action": "delete",
            "path": this.props.item.local_path
        };
        dispatch(actions.setIsLoadingTrue());
        axios.put(`/api/courses/${course_id}/`, data, {'headers':{'Authorization': 'Token ' + localStorage.token}}).then((res)=> {
            axios.get(`/api/courses/${course_id}/`, {'headers':{'Authorization': 'Token ' + localStorage.token}}).then((res) => {
                console.log("___");
                console.log(res);
                const course_data = res.data;
                dispatch(actions.setCourseStructure(course_id, course_data));
                this.handleClose();
                setTimeout( () => {dispatch(actions.setIsLoadingFalse())}, 1000);
            }).catch((res) => {
                console.log(res);
                alert("Error fetching course data")
            });
        }).catch((res)=> {
            console.log(res.data);
        });
    }

    render() {
        const classes = "pt-card pt-elevation-4 docs-overlay-example-transition pt-overlay-content tudor-popup";
        const selected = this.props.item;
        return (
            <div>
                { selected ?
                    <Overlay onClose={this.handleClose} isOpen={this.props.state.main.deleteItemPopup}>
                        <div className={classes} >
                            <h3>Delete Object</h3>
                            <p>
                                Are you sure you want to delete: {this.props.item.name}
                            </p>
                            <br />
                            <Button intent={Intent.DANGER} onClick={this.handleClose}>Cancel</Button>
                            <Button onClick={this.handleDelete} style={{ float: "right" }}>Delete</Button>
                        </div>
                    </Overlay>
                    :
                    <div></div>
                }
            </div>
        );
    }

}
