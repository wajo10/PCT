const axios = require('axios');
var promise = require('bluebird');
const path = require("path");
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
                .send(msg);
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

function start_logging(req, res, next) {
    socket.emit("Command", "StartLogging");
    socket.on('StartResult', function (msg) {
        console.log(msg);
        res.status(200)
            .json({
                status: 'success',
                data: msg
            });
        socket.removeAllListeners("StartResult")
    });
}

function stop_logging(req, res, next) {
    socket.emit("Command", "StopLogging");
    socket.on('StopResult', function (msg) {
        console.log(msg);
        res.status(200)
            .json({
                status: 'success',
                data: msg
            });
        socket.removeAllListeners("StopResult")
    });
}

function send_file(req, res, next) {
    var options = {
        root: path.join(__dirname,"..")
    };
    var fileName = 'register.csv';
    res.sendFile(fileName, options, function (err) {
        if (err) {
            next(err);
        } else {
            console.log('Sent:', fileName);
        }
    });
}

module.exports = {
    updateSock: updateSock,
    getAll: getAll,
    set_setValues: set_setValues,
    send_file: send_file,
    start_logging: start_logging,
    stop_logging: stop_logging,
};
