const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path')
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
    exec('python ../pyRCV.py temp/temp.csv temp/results/temp-results.csv', (error, stdout, stderr) => {
        if (error) {
            console.log(error);
            console.log(stderr);
            res.status(500)
            res.send('problem processing votes file')
        } else {
            const files = fs.readdirSync('temp/results')
            var data = ''
            for (var i = 0; i < files.length; i++){
                data += `"round-${i}":`
                data += fs.readFileSync(path.resolve(`temp/results/${files[i]}`));
                if (i + 1 !== files.length){
                    data += ',';
                }
            }
            res.send(`{${data}}`);
        }
        
    });
});

const server = app.listen(port, () => {
    console.log(`pyRCV listening at http://${server.address().address}:${server.address().port}`);
});