import React, { Component } from 'react';
import "./Settings.css";

var methods = [ "Graph", "TFISF"]

class Settings extends Component {
    constructor(props) {
        super(props);

        var currentMethod, currentCompressionFactor;
        if(this.props.currentSettings){
            currentMethod = this.props.currentSettings.method;
            currentCompressionFactor = this.props.currentSettings.compressionFactor;
        }
        this.state = {
            method: (currentMethod ? currentMethod : methods[0]),
            compressionFactor: (currentCompressionFactor ? currentCompressionFactor : 0.8)
        }
        this.settingsUpdated = this.settingsUpdated.bind(this);
        this.closeSettings = this.closeSettings.bind(this);
    }

    settingsUpdated(event) {
        var toUpdate = this.state;

        if(event.target.nodeName === "SELECT") {
            toUpdate.method = event.target.value;
        } else if(event.target.nodeName === "INPUT") {
            switch (event.target.id) {
                case "compression-scale":
                    toUpdate.compressionFactor = event.target.value / 100.0
                    break
                default:
                    break
            }
        }
        this.setState(toUpdate)
        this.props.onSettingsUpdated(toUpdate);
    }

    closeSettings(event) {
        this.props.onSettingsClosed(this);
    }

    render() {
        return (
            <div className="Settings-View">
                <h4>How do you like your Summary?</h4>
                <table>
                    <tbody>
                        <tr>
                            <td><span>Summary Method</span></td>
                            <td>
                                <select onChange={ this.settingsUpdated } value={ this.state.method }>
                                    {
                                        methods.map((method) => {
                                            return <option key={method} value={method}>{method}</option>
                                        })
                                    }
                                </select>
                            </td>
                        </tr>
                        <tr>
                            <td><span>Compression Scale</span></td>
                            <td>
                                <input id="compression-scale" type="range" min="0" max="100" value={this.state.compressionFactor * 100} onChange={ this.settingsUpdated }/>
                            </td>
                            <td id="compression-scale-text">
                                <span>{this.state.compressionFactor}</span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <button onClick={ this.closeSettings } >Close</button>
            </div>

        );
    }
}

export default Settings;
