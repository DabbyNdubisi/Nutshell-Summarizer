import React, { Component } from 'react';
import spinner from "./spinner.svg";
import "./MenuActionComponent.css";

class MenuActionComponent extends Component {
    render() {
        let element = null;
        if(this.props.loading) {
            element = <img src={spinner} className="MenuAction-spinner" alt="logo"  />
        } else {
            element = <p className="MenuAction-text">{this.props.actionText}</p>
        }

        return (
            <div className={`MenuAction ${this.props.loading ? "Loading" : "Idle"}`} onClick={this.props.onClick}>
                { element }
            </div>
        );
    }
}

export default MenuActionComponent;
