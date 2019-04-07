const url = require('url');
const path = require('path');
const {
    app,
    BrowserWindow,
    //Menu
} = require('electron');
let {PythonShell} = require('python-shell')


function createWindow() {
    PythonShell.run('app.py',{args:["./test_set"]}, function (err, results) {
        if (err) throw err;
        console.log('hello.py finished.');
        console.log('results', results);
    });
    window = new BrowserWindow({
        width: 800,
        height: 600
    });
    window.loadFile("index.html");
}

app.on('ready', function(){
    // Create new window
    createWindow = new BrowserWindow({});
    createWindow.loadURL(url.format({
        pathname: path.join(__dirname, 'index.html'),
        protocol:'file:',
        slashes: true
    }));


});


app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});