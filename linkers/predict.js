class Store {
    constructor() {
        this.store = {}
    }
    addItem(name, path) {
        this.store[name] = path;
    }

    getItem() {
        return this.store;
    }
}

var trainingFolders = new Object();

const predictImage = () => {
    try {
        const predict = new PythonShell('app.py train', options);
        predict.end((err, code, message) => {
            console.log(err, code, message)
        })
    } catch (error) {
        console.log(error)
    }
}

function addGroup(event, clast) {
    // var trainingFolders = new Object();
    // const files = event.target.files;
    // var folder;
    // folder = files[0];
    // folder = folder.webkitRelativePath;
    console.log('Saving Directory')
    console.log(store.getItem());
    console.log('Saved Directory')
}

function train() {
    console.log('train');
}

function predict() {
    var {
        PythonShell
    } = require("python-shell");
    var path = require('path');
    var options = {
        scriptPath: path.join(__dirname, '/../server'),
        pythonPath: '/usr/local/bin/python3',
        args : ['predict', '-path', '../testimages/nh3.jpg']
    }

    try {
        const predict = new PythonShell('app.py', options);
        predict.end((err, code, message) => {
            console.log(err, code, message)
        })
    } catch (error) {
        console.log(error)
    }
}

predict()