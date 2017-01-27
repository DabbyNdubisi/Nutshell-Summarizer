import React, { Component } from 'react';
import "./TextComponent.css";

class TextComponent extends Component {
    constructor(props) {
        super(props);
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event) {
        this.props.onChange(event.target.value);
    }

    render() {
        const editable = this.props.editable;
        const value = this.props.value;
        const placeholder = this.props.placeholder;

        return (
            <div className="TextComponent">
                <textarea className="TextComponent-textarea" placeholder={placeholder}
                    value={value} onChange={editable ? this.handleChange : null } disabled={!editable} />
            </div>
        );
    }
}

export default TextComponent;
