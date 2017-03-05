import React, { Component } from 'react';
import "./Header.css";

class Header extends Component {
    constructor(props) {
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(event) {
        this.props.onSettingsClicked();
    }

    render() {
        return (
            <div className="Header-Nav">
                <div className="Header-item title-area">
                    <h1 className="Header-title">In a NutShell</h1>
                    <p className="Header-subtext">Shorter is the new black</p>
                </div>
                <ul className="Header-item actions-area">
                    <li><button onClick={ this.handleClick }>Settings</button></li>
                </ul>
            </div>
        );
    }
}

export default Header;
