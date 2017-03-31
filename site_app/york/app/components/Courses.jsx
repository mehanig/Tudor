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
import AuthHelper from "../components/AuthHelper"

@connect(state => ({state}))
export default class Courses extends React.Component {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
        const token = this.props.state.main.globalHeaderToken;
        const {dispatch} = this.props;
        axios.get('/api/courses', {'headers':{'Authorization': 'Token ' + localStorage.token}}).then((res)=>{
            dispatch(actions.setCourses(res.data));
        }).catch((res)=> {
            console.log(res.data);
        });
    }

    render() {
        const courses = this.props.state.main.courses;
        return (
            <div>
                <div><h3>List of your Courses</h3></div>
                {courses.map(function(course) {
                    const url = `/course/${course.key.toString()}`;
                    return <Link to={url} key={course.key.toString()}><div className="pt-card pt-elevation-0 pt-interactive course-card__main">
                        <h5>{course.name}</h5>
                    </div></Link>
                })}
            </div>
        )
    }

}
