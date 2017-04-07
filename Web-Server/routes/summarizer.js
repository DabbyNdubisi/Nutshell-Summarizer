var express = require('express');
var path = require('path');
var router = express.Router();

var spawn = require("child_process").spawn;

/* GET users listing. */
router.post('/', function(req, res, next) {
    new Promise(function(resolve, reject) {
        if(req.files) {
            req.body.filepath = req.files[0].path;
        }
        resolve();
    })
        .then(function() {
            var data = {};
            if(req.body.toSummarize || req.body.filepath) {
                const text = req.body.toSummarize || "";
                const method = req.body.method;
                const compressionFactor = req.body.compressionFactor;
                const filepath = req.body.filepath;
                var args = [path.resolve(__dirname, '../summarizer/summarize.py'), method, compressionFactor];
                console.log(args);
                if(filepath) {
                    args.push(text);
                    args.push(filepath);
                } else {
                    args.push(text);
                }
                const process = spawn('python', args);
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
        })
});

module.exports = router;
