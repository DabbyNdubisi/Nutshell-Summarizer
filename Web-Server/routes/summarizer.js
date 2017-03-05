var express = require('express');
var path = require('path');
var router = express.Router();

var spawn = require("child_process").spawn;

/* GET users listing. */
router.post('/', function(req, res, next) {
    var data = {};
    if(req.body.toSummarize) {
        const text = req.body.toSummarize;
        const method = req.body.method;
        const compressionFactor = req.body.compressionFactor;
        const process = spawn('python', [path.resolve(__dirname, '../summarizer/summarize.py'), method, compressionFactor, text]);
        var summary = "";
        process.stdout.on('data', function(data) {
            summary += data
        });
        process.on('close', function(code) {
            data.summary = summary;
            res.send(data);
        })
    } else {
        data.error = "No text received"
        res.send(data);
    }
});

module.exports = router;
