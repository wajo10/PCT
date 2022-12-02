const axios = require('axios');
var promise = require('bluebird');
var socket = undefined;

var options = {
    // Initialization Options
    promiseLib: promise
};




function updateSock(sock) {
    socket = sock;
}


function setRelays(req, res, next) {
    let command = req.params.command;
    let id = req.params.id;
    let send = `relay,${command},${id}`;
    socket.emit("Command", send);
    socket.on('RelayResult', function (msg) {
        console.log(msg);
        res.status(200)
            .json({
                status: 'success',
                data: msg
            });
        socket.removeAllListeners("RelayResult")
    });
}

function getAll(req, res, next) {
    socket.emit("Command", "All");
    socket.on('Result', function (msg) {
        console.log(msg);
        if (msg !== "Error") {
            res.status(200)
                .json({
                    status: 'success',
                    data: msg
                });
        } else {
            res.status(504)
                .json({
                    status: 'Error, No Data Received',
                })
        }
        socket.removeAllListeners("Result")
    });
}

function set_setValues(req, res, next) {
    let command = req.params.command;
    let value = req.params.value;
    let send = `${command},${value}`;
    socket.emit("Command", send);
    socket.on('SetResult', function (msg) {
        console.log(msg);
        res.status(200)
            .json({
                status: 'success',
                data: msg
            });
        socket.removeAllListeners("SetResult")
    });
}

module.exports = {
    updateSock: updateSock,
    getAll: getAll,
    set_setValues: set_setValues
};
