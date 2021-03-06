import React, { Component } from 'react';
import Header from './Header';
import TextComponent from './TextComponent';
import Settings from './Settings';
import MenuActionComponent from './MenuActionComponent';
import './App.css';

var utility = require('./Utility');
var $ = require('jquery');
var ROOT_URL = "http://localhost:3001/api";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawText: "",
            summarizedText: "",
            isSummarizing: false,
            isSettingsVisible: false,
            settings: {
                method: "Graph",
                compressionFactor: 0.8
            }
        }

        this.rawTextChanged = this.rawTextChanged.bind(this);
        this.summarize = this.summarize.bind(this);
        this.uploadFile = this.uploadFile.bind(this);
        this.showSettings = this.showSettings.bind(this);
        this.hideSettings = this.hideSettings.bind(this);
        this.updateSettings = this.updateSettings.bind(this);
    }

    render() {
        let isSummarizing = this.state.isSummarizing;
        let settingsView = this.state.isSettingsVisible ?
            <div className="App-Settings" ref={ (value) => { this.settingsView = value } }>
                <Settings currentSettings={ this.state.settings } onSettingsUpdated={ this.updateSettings } onSettingsClosed={ this.hideSettings }/>
            </div> : null;
        if (this.settingsView) {
            this.settingsView.style.display = "block"
        }

        return (
            <div className="App">
                <div className="App-Header">
                    <Header onSettingsClicked={ this.showSettings }/>
                </div>
                { settingsView }
                <div className="App-Content">
                    <div className="App-Content-Left">
                        <TextComponent editable={isSummarizing ? false : true } placeholder={"Enter a text to summarize here"} value={this.state.rawText} onChange={this.rawTextChanged} />
                        <div className="App-MenuActions">
                            { this.shouldShowSummarizeAction() ?
                                <div className="App-Menu-Action">
                                    <MenuActionComponent onClick={ isSummarizing ? null : this.summarize } loading={ isSummarizing } actionText="Summarize" />
                                </div> : null
                            }
                            { !this.shouldShowSummarizeAction() ?
                                <div className="App-Menu-Action">
                                    <input type="file" name="file" accept=".txt" onChange={ (event) => { this.setState({ files: event.target.files }) } }/>
                                    { (this.state.files && this.state.files.length > 0) ?
                                        <div className="App-Menu-Action">
                                            <MenuActionComponent onClick={ isSummarizing ? null : this.uploadFile } loading={ isSummarizing } actionText="Summarize File" />
                                        </div> : null
                                    }
                                </div> : null
                            }

                        </div>
                    </div>
                    <div className="App-Content-Right">
                        <TextComponent editable={false} placeholder={"Your summary shows up here"} value={this.state.summarizedText} />
                    </div>
                </div>
            </div>
        );
    }

    rawTextChanged(text) {
        console.log("Raw text changed!");
        this.setState({ rawText: text });
    }

    shouldShowSummarizeAction() {
        return this.state.rawText.length > 0;
    }

    summarize() {
        let text = this.state.rawText;
        this.setState({ isSummarizing: true });
        let weakThis = this;
        return $.ajax({
            type: 'POST',
            url: ROOT_URL,
            data: {
                toSummarize: text,
                method: this.state.settings.method,
                compressionFactor: this.state.settings.compressionFactor
            },
        })
        .done(function(data) {
            weakThis.setState({ isSummarizing: false, summarizedText: data.summary });
        })
        .fail(function(error) {
            console.log(JSON.stringify(error));
            weakThis.setState({ isSummarizing: false, summarizedText: '' });
        })
    }

    uploadFile() {
        let file = this.state.files[0];
        this.setState({ isSummarizing: true });
        let weakThis = this;
        let data = new FormData();
        data.append("file", file);
        data.append("method", this.state.settings.method);
        data.append("compressionFactor", this.state.settings.compressionFactor);
        return $.ajax({
            type: 'POST',
            url: ROOT_URL,
            data: data,
            dataType: 'json',
            processData: false,
            contentType: false,
        })
        .done(function(data) {
            weakThis.setState({ isSummarizing: false, summarizedText: data.summary });
        })
        .fail(function(error) {
            console.log(JSON.stringify(error));
            weakThis.setState({ isSummarizing: false, summarizedText: '' });
        })
    }

    hideSettings() {
        this.setState({ isSettingsVisible: false });
    }

    showSettings() {
        this.setState({ isSettingsVisible: !this.state.isSettingsVisible })
    }

    updateSettings(settings) {
        this.setState({
            settings: settings
        })
    }
}

export default App;
