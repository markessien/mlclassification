const { app, BrowserWindow } = require('electron');
var fs = require('fs');
let { PythonShell }= require('python-shell')
const {ipcMain} = require('electron')

ipcMain.on('datasetRecovery', (event, arg) => {
    let results = [];
    console.log(arg[0])

    fs.readdirSync(arg[0], function (err, list) {
        list.forEach(function (file) {
            file = path.resolve(dir, file);

            fs.stat(file, function (err, stat) {
                if (stat.isDirectory()) {
                    // console.log(file)
                    results.push(file);
                }
            });

        });
        

    });
    console.log(results)

});

function createWindow() {
    // PythonShell.run('app.py',{args:["./test_set"]}, function (err, results) {
    //     if (err) throw err;
    //     console.log('hello.py finished.');
    //     console.log('results', results);
    // });
    window = new BrowserWindow({
        width: 800,
        height: 600
    });
    window.loadFile("index.html");
}

app.on('ready', createWindow);

app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});