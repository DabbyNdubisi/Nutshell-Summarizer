import React, { Component } from 'react';
import "./Header.css";

class Header extends Component {
    render() {
        return (
            <div className="Header-Nav">
                <h1 className="Header-title">In a NutShell</h1>
                <p className="Header-subtext">Shorter is the new black</p>
            </div>
        );
    }
}

export default Header;
