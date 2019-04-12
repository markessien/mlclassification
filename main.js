const { app, BrowserWindow } = require('electron');
var fs = require('fs');
let { PythonShell }= require('python-shell')
const {ipcMain} = require('electron')
const path = require('path');
let window;
const url = require('url');

ipcMain.on('trainingDatasetRecovery', (event, arg) => {
    var dir = arg[0]
    console.log(dir)
    var results = [];
    var list = fs.readdirSync(dir);

    list.forEach(function (file) {
        file = path.resolve(dir, file);
        var fileStats = fs.statSync(file);
        if (fileStats.isDirectory()){
            file = file.split('/');
            results.push(file[file.length-1]);
        }
    })
    event.sender.send('trainingDatasets',results)
});

ipcMain.on('testDatasetRecovery', (event, arg) => {
    var dir = arg[0]
    console.log(dir)
    var results = [];
    var list = fs.readdirSync(dir);

    list.forEach(function (file) {
        file = path.resolve(dir, file);
        var fileStats = fs.statSync(file);
        if (fileStats.isDirectory()){
            file = file.split('/');
            results.push(file[file.length-1]);
        }
    })
    event.sender.send('testDatasets',results)
});

function createWindow() {
    // PythonShell.run('app.py',{args:["./test_set"]}, function (err, results) {
    //     if (err) throw err;
    //     console.log('hello.py finished.');
    //     console.log('results', results);
    // });
    window = new BrowserWindow({
        width: 1000,
        height: 600
    });
    window.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: 'file',
        slashes: true
    }));
  
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (window == 'null') {
        createWindow();
    }
});
