const express = require("express");

const router = express();
const port = 3031;
var queries = require('./queries');
var path = require('path');
var cookieParser = require('cookie-parser');
const http = require('http').createServer(router);

let server = http.listen(port, () => {
    console.log("El servidor está inicializado en el puerto: ", port);

});

// Sockets
const io = require('socket.io')(server,{
    allowEIO3: true
});

router.get('/', (req, res) => {
    res.status(200)
        .json({
            status: 'success',
            data: "Connection Established",
            message: 'SPD Materiales '
        });
});

//Whenever someone connects this gets executed
io.on('connection', (socket) => {
    socket.emit('Whatever',"Message");
    console.log('an user connected');

    // Send Socket to Queries File
    queries.updateSock(socket);

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});



router.set('views', path.join(__dirname, 'views'));
router.set('view engine', 'jade');

router.use(express.json());
router.use(express.urlencoded({ extended: false }));
router.use(cookieParser());
router.use(express.static(path.join(__dirname, 'public')));

router.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    res.header('Access-Control-Allow-Methods', 'PUT, POST, GET, DELETE, OPTIONS');
    next();
});

// Routes
router.get('/api/SPD/All/', queries.getAll); //Get all parameters
router.get('/api/SPD/setValues/:command/:value', queries.set_setValues); //Set point values

router.get('/', async (req, res) => {
    res.render('index', {title: 'SPD Server'}); // load the single view file (angular will handle the page changes on the front-end)

});
module.exports = {router};
