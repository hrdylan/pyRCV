const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const exec = require("child_process").exec;

const app = express();
const port = 4000;

app.use(express.text());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "http://localhost:3000"); 
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
  });

app.get('/', (req, res) => {
    res.send('hello world');
});

app.post('/pyRCV', (req, res) => {
    console.log(req.body);
    fs.writeFile('./temp/temp.csv', req.body, (err) => {
        if (err) { console.log(err) };
        console.log('file recv and writen to disk');
    });
    exec('ls && python ../pyRCV.py temp/temp.csv temp/temp-results.csv', (error, stdout, stderr) => {
        if (error) {
            console.log(error);
        }
        if (stdout) {
            console.log(stdout);
        }
        if (stderr) {
            console.log(stderr);
        }
        
    });
    process.stdout.on('data', data => { 
        console.log(data.toString());
    }); 
    process.on('error', (error) => {
        console.log(error);
    });

    res.send('body recv');
});

const server = app.listen(port, () => {
    console.log(`pyRCV listening at http://${server.address().address}:${server.address().port}`);
});