const {
    PythonShell
} = require("python-shell");
const path = require('path');
const options = {
    scriptPath: path.join(__dirname, '/../server'),
    pythonPath: '/usr/local/bin/python3'
}
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

function addGroup(input) {
    console.log(input, document.getElementById('files').value);

}


function train() {
    console.log('train');
}

function predict() {
    console.log('predict');
}