var express = require('express');
var path = require('path');
var router = express.Router();


/* SERVE static HTML index page */
router.get('*', function(req, res, next) {
    res.sendFile(path.join(__dirname, '../public', 'index.html')); // load our public/index.html file
});

module.exports = router;
