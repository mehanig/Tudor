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
    }

    componentDidMount() {
        const token = this.props.state.main.globalHeaderToken;
        const {dispatch} = this.props;
        axios.get('/api/courses', {'headers':{'Authorization': 'Token ' + token}}).then((res)=>{
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
                    return <div className="pt-card pt-elevation-0 pt-interactive course-card__main" key={course.key.toString()}>
                        <Link to={url}><h5>{course.name}</h5></Link>
                    </div>
                })}
            </div>
        )
    }

}
