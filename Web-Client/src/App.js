import React, { Component } from 'react';
import Header from './Header';
import TextComponent from './TextComponent';
import MenuActionComponent from './MenuActionComponent';
import './App.css';

var utility = require('./Utility');

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            rawText: "",
            summarizedText: "",
            isSummarizing: false
        }

        this.rawTextChanged = this.rawTextChanged.bind(this);
        this.summarize = this.summarize.bind(this);
    }

    render() {
        let isSummarizing = this.state.isSummarizing;
        // let currentMenuAction = this.shouldShowActionMenu() ?
        //     <div className={`App-menu ${isSummarizing ? "App-menu-spinner" : "App-menu-btn_Summarize"}`}
        //         onClick={isSummarizing ? null :  }>
        //         { isSummarizing ? <img src={spinner} className="App-spinner" alt="logo"  /> : "Summarize" }
        //     </div> : null;

        return (
            <div className="App">
                <div className="App-Header">
                    <Header />
                </div>
                <div className="App-Content">
                    <div className="App-Content-Left">
                        <TextComponent editable={isSummarizing ? false : true } placeholder={"Enter a text to summarize here"} value={this.state.rawText} onChange={this.rawTextChanged} />
                        { this.shouldShowActionMenu() ?
                            <div className="App-MenuAction">
                                <MenuActionComponent onClick={ isSummarizing ? null : this.summarize } loading={ isSummarizing } actionText="Summarize" />
                            </div> :
                            null
                        }
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

    shouldShowActionMenu() {
        return this.state.rawText.length > 0;
    }

    summarize() {
        let text = this.state.rawText;
        this.setState({ isSummarizing: true });
        let weakThis = this;
        //TODO: Invoke summary from server
        return utility.delay(5000)
            .then(() => {
                let text = "This is your summarized text."
                weakThis.setState({ isSummarizing: false, summarizedText: text });
            });
    }
}

export default App;
