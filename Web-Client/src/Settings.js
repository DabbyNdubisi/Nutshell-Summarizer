import React, { Component } from 'react';
import "./Settings.css";

var methods = [ "Graph", "TFISF"]

class Settings extends Component {
    constructor(props) {
        super(props);

        this.state = {
            method: methods[0],
            compressionFactor: 0.8
        }

        this.settingsUpdated = this.settingsUpdated.bind(this);
        this.closeSettings = this.closeSettings.bind(this);
    }

    settingsUpdated(event) {
        var toUpdate = this.state;

        if(event.target.nodeName == "SELECT") {
            toUpdate.method = event.target.value;
        } else if(event.target.nodeName == "INPUT") {
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
                                <select onChange={ this.settingsUpdated }>
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
                                <input id="compression-scale" type="range" onChange={ this.settingsUpdated }/>
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
