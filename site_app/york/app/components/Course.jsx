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

import ItemControls from "../components/ItemControls"

import { Classes, ITreeNode, Tooltip, Tree } from "@blueprintjs/core";

@connect(state => ({state}))
export default class Courses extends React.Component {
    constructor(props) {
        super(props);
        const courses = this.props.state.main.courses;
        const id = this.props.match.params.id;
        const course = courses.find((el) => el.key == id);
        // const tooltipLabel = <Tooltip content="An eye!"><span className="pt-icon-standard pt-icon-eye-open"/></Tooltip>;
        const longLabel = "Organic meditation gluten-free, sriracha VHS drinking vinegar beard man.";
        this.state = {course_name: course.name, nodes: course.lessons, displaySelected: null};

        // UPDATE TO ITREE SCHEMA
        this.state.nodes.map((l) => {
            l.label = l.name;
            l.key = l.name;
            l.iconName = "box";
            l.childNodes = l.steps;
            l.hasCaret = false;
            l.isSelected = false;
            l.childNodes.map((step) => {
                step.label = step.name;
                step.iconName = "folder-close";
                step.childNodes = step.substeps;
                step.hasCaret = false;
                step.isSelected = false;
                if (step.childNodes.length) {
                    step.hasCaret = true;
                }
                step.childNodes.map((ss) => {
                    ss.label = ss.name;
                    ss.iconName = "film";
                    step.isSelected = false;
                    if (ss.substep_screen || ss.substep_camera) {
                        ss.hasCaret = true;
                        ss.childNodes = [];
                        if (ss.substep_screen) {
                            ss.childNodes.push({label: "screen_cast", iconName: "desktop"});
                        }
                        if (ss.substep_camera) {
                            ss.childNodes.push({label: "camera", iconName: "camera"});
                        }
                    }
                });
            });
            if (!l.childNodes.length) {
                l.label += "   (empty)";
            } else {
                l.hasCaret = true;
            }
        });
        let i = 0;
        this.forEachNode(this.state.nodes, (n) => n.id = i++);

        this.handleNodeClick = this.handleNodeClick.bind(this);
        this.handleNodeCollapse = this.handleNodeCollapse.bind(this);
        this.handleNodeExpand = this.handleNodeExpand.bind(this);
        this.handleDoubleClick = this.handleDoubleClick.bind(this);
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

    delayedSelectedUpdate(nodeData) {
        if (nodeData) {
            setTimeout((nodeData) => {
                if (this.state.selectedNotShown && this.state.selectedNotShown.local_path === nodeData.local_path) {
                    this.setState({...this.state, displaySelected: nodeData})
                }
            }, 600, nodeData);
        } else {
            setTimeout(() => this.setState({...this.state, displaySelected: false, selectedNotShown: null}), 500);
        }
    }

    //TODO: Refactor it!
    componentWillReceiveProps(nextProps) {
        const id = nextProps.match.params.id;
        const courses = nextProps.state.main.courses;
        const course = courses.find((el) => el.key == id);
        if (JSON.stringify(course.lessons) !== JSON.stringify(this.state.nodes)) {
            console.log("DIFF!!!");
            let nodes = course.lessons;
            nodes.map((l) => {
                l.label = l.name;
                l.key = l.name;
                l.iconName = "box";
                l.childNodes = l.steps;
                l.hasCaret = false;
                l.isSelected = false;
                l.childNodes.map((step) => {
                    step.label = step.name;
                    step.iconName = "folder-close";
                    step.childNodes = step.substeps;
                    step.hasCaret = false;
                    step.isSelected = false;
                    if (step.childNodes.length) {
                        step.hasCaret = true;
                    }
                    step.childNodes.map((ss) => {
                        ss.label = ss.name;
                        ss.iconName = "film";
                        step.isSelected = false;
                        if (ss.substep_screen || ss.substep_camera) {
                            ss.hasCaret = true;
                            ss.childNodes = [];
                            if (ss.substep_screen) {
                                ss.childNodes.push({label: "screen_cast", iconName: "desktop"});
                            }
                            if (ss.substep_camera) {
                                ss.childNodes.push({label: "camera", iconName: "camera"});
                            }
                        }
                    });
                });
                if (!l.childNodes.length) {
                    l.label += "   (empty)";
                } else {
                    l.hasCaret = true;
                }
            });

            let i = 0;
            this.forEachNode(nodes, (n) => n.id = i++);

            this.setState({
                ...this.state,
                course_name: course.name,
                nodes
            });
        }
    }

    handleNodeClick(nodeData, _nodePath, e) {
        const originallySelected = nodeData.isSelected;
        this.forEachNode(this.state.nodes, (n) => n.isSelected = false);
        nodeData.isSelected = originallySelected == null ? true : !originallySelected;
        if (nodeData.isSelected) {
            this.delayedSelectedUpdate(nodeData);
            this.setState({...this.state, selectedNotShown: nodeData});
        } else {
            this.delayedSelectedUpdate(null);
            this.setState({...this.state, selectedNotShown: null});
        }
    }

    handleNodeCollapse(nodeData) {
        nodeData.isExpanded = false;
        this.setState(this.state);
    }

    handleNodeExpand(nodeData) {
        nodeData.isExpanded = true;
        this.setState(this.state);
    }

    handleDoubleClick(nodeData) {
        if (nodeData.isExpanded) {
            this.handleNodeCollapse(nodeData);
        } else {
            this.handleNodeExpand(nodeData);
        }
        this.setState(this.state);
    }
    render() {
        return (
            <div>
                <div><h3>{this.state.course_name}</h3></div>
            <ItemControls item={this.state.displaySelected} course_id={this.props.match.params.id}/>
            <Tree
                contents={this.state.nodes}
                onNodeClick={this.handleNodeClick}
                onNodeCollapse={this.handleNodeCollapse}
                onNodeExpand={this.handleNodeExpand}
                onNodeDoubleClick={this.handleDoubleClick}
                className={Classes.ELEVATION_0}
            />
            </div>
        )
    }

    forEachNode(nodes, callback) {
        if (nodes == null) {
            return;
        }
        for (let node of nodes) {
            callback(node);
            this.forEachNode(node.childNodes, callback);
        }
    }
}
