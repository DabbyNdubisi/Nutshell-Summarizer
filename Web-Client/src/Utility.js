module.exports = {
    delay: delay
};

function delay(duration) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
            resolve();
        }, duration);
    });
}
