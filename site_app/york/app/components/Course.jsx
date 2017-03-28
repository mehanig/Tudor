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

@connect(state => ({state}))
export default class Courses extends React.Component {
    constructor(props) {
        super(props);
        const courses = this.props.state.main.courses;
        const id = this.props.match.params.id;
        const course = courses.find((el) => el.key == id);
        this.state = {course};
    }

    componentDidMount() {
        const token = this.props.state.main.globalHeaderToken;
        const {dispatch} = this.props;
        axios.get('/api/courses', {'headers': {'Authorization': 'Token ' + token}}).then((res) => {
            dispatch(actions.setCourses(res.data));
        }).catch((res) => {
            console.log(res.data);
        });
    }

    render() {
        return (
            <div>
                <div><h3>{this.state.course.name}</h3></div>
                {this.state.course.lessons.map((lesson) => {
                    return (
                        <div className="pt-tree pt-elevation-0 lesson-folder__main">
                            <ul className="pt-tree-node-list pt-tree-root">
                                <li className="pt-tree-node pt-tree-node-expanded">
                                    <div className="pt-tree-node-content">
                                        <span
                                            className="pt-tree-node-caret pt-tree-node-caret-open pt-icon-standard"></span>
                                        <span
                                            className="pt-tree-node-icon pt-icon-standard pt-icon-folder-close"></span>
                                        <span className="pt-tree-node-label">{lesson.name}</span>
                                        <span className="pt-tree-node-secondary-label">Last Edit: </span>
                                    </div>
                                    <ul className="pt-tree-node-list">
                                        {lesson.steps.map((step) => {
                                           return (
                                            <li className="pt-tree-node">
                                                <div className="pt-tree-node-content">
                                                    <span className="pt-tree-node-caret-none pt-icon-standard"></span>
                                                    <span
                                                    className="pt-tree-node-icon pt-icon-standard pt-icon-document"></span>
                                                    <span className="pt-tree-node-label">{step.name}</span>
                                                </div>
                                            </li>
                                           )
                                        })}
                                    </ul>
                                </li>
                            </ul>
                        </div>
                    )
                })}
            </div>
        )
    }

}
