var {
    PythonShell
} = require("python-shell");
var path = require('path');
var readline = require('readline');
var fs = require('fs');


class Store {
    constructor() {
        this.groups = {}
        this.predict = {}
    }
    addGroup(name, path) {
        this.groups[name] = path;
    }
    addPredict(path) {
        this.predict.path = path;
    }
    getGroup() {
        return this.groups;
    }
    getPredict() {
        return this.predict;
    }
    validateGroup() {
        if (this.groups.groupa && this.groups.groupb) {
            return true;
        }
        return false
    }
    clearGreat() {
        this.groups = {};
    }
}

const store = new Store();


function addGroup(event, clast) {
    const files = event.target.files;
    var folder = files[0].path;
    folder = folder;
    store.addGroup(clast, folder);
    document.getElementById(`visible${clast}`).placeholder = folder;
    store.validateGroup() === true ? document.getElementById(`trainbutton`).disabled = false : null;
}

function addPredict(event) {
    const files = event.target.files;
    var folder = files[0];
    folder = folder.path;
    store.addPredict(folder)
    document.getElementById(`predictinput`).placeholder = folder;
    const options = {
        mode: 'text',
        scriptPath: './server',
        pythonPath: '/usr/local/bin/python3',
        args: ['retrieve_models']
    }
    PythonShell.run('app.py', options, (err, results) => {

        Swal.fire({
            html: `<br/><span>This prediction will be done using your default model</span>`,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: 'Proceed',
            preConfirm: () => {
                return [
                    predict(folder)
                ]
            },
            cancelButtonText: '<i class="fa fa-thumbs-down"></i> Cancel',
        })
    });
}


function predict(folder) {
    console.log('hello');
    const perc = 30;
    document.getElementById('predictprogress').value = perc;
    document.getElementById('predicttag').innerText = `${perc}%`;
    try {
        const options = {
            mode: 'text',
            scriptPath: './server',
            pythonPath: '/usr/local/bin/python3',
            args: ['predict', '-path', `${folder}`]
        }
        PythonShell.run('app.py', options, (err, results) => {
            if (err) throw err;
            // results is an array consisting of messages collected during execution
            console.log('results: %j', results);
            //todo: If api returns the results and the folder directory
            Swal.fire({
                html: `<span>${results}</span>`,
                showCloseButton: false,
                showCancelButton: false,
                focusConfirm: false
            })
            const perc = 100;
            document.getElementById('predictprogress').value = perc;
            document.getElementById('predicttag').innerText = `${perc}%`;
            document.getElementById('predictresult').innerText = 'Completed';
            const slides = document.getElementById(`sliders`);
            fs.readdir(folder, function (err, files) {
                //handling error
                if (err) {
                    return console.log('Unable to scan directory: ' + err);
                }
                //listing all files using forEach
                document.getElementById(`slides`).hidden = false;
                files.forEach(function (file) {
                    const img = document.createElement("img");
                    file.split('.').length > 1 ? img.src = `${folder+'/'+file}` : null;
                    img.className = "mySlides"
                    img.style = "width:100%; height:250px;";
                    slides.appendChild(img)
                });
                showDivs(5);
            });

        });
    } catch (error) {
        console.log(error)
    }
}

function showDivs(n) {
    let i;
    var x = document.getElementsByClassName("mySlides");
    if (n > x.length) {
        slideIndex = 1
    }
    if (n < 1) {
        slideIndex = x.length
    }
    for (i = 0; i < x.length; i++) {
        x[i].style.display = "none";
    }
    x[slideIndex - 1].style.display = "block";
    var y = document.getElementById("confidencetext");
    updateConfidenceProgress("confidence", 'progress--100')
    y.innerText = '100%'

}

function updateConfidenceProgress(id, name) {
    var element, name, arr;
    element = document.getElementById(id);
    arr = element.className.split(" ");
    element.className = arr[0] + " " + name;
}

function train() {
    document.getElementById(`trainbutton`).disabled = true;
    const textareavalue = document.getElementById(`modelname`).value;
    const modelname = textareavalue.split('').length > 1 ? textareavalue : makeid(8);
    console.log('Saving Directory');
    const groups = store.getGroup();
    Swal.fire({
        html: `<span>You are about to train a model with name <b>${modelname}</b></span>`,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Proceed',
        onClose: () => {
            return [
                startTraining(groups, modelname)
            ]
        },
        cancelButtonText: '<i class="fa fa-thumbs-down"></i> Cancel',
    })
}

function startTraining(groups, modelname) {
    const groupa = groups.groupa;
    const groupb = groups.groupb;
    const options = {
        mode: 'text',
        scriptPath: './server',
        pythonPath: '/usr/local/bin/python3',
        args: ['train', '--grpA', `${groupa}`, '--grpB', `${groupb}`, '--model', `${modelname}`]
    }
    try {
        let pyshell = new PythonShell('app.py', options);
        pyshell.send('');
        pyshell.on('message', function (message) {
            Swal.fire({
                html: `<span>${message}</span>`,
                showCloseButton: false,
                showCancelButton: false,
                focusConfirm: false
            })
        });
        pyshell.end(function (err, code, signal) {
            if (err) {
                document.getElementById(`trainbutton`).disabled = false
                Swal.fire({
                    html: `<span>${err}</span>`,
                    showCloseButton: false,
                    showCancelButton: false,
                    focusConfirm: false
                })
            }
            Swal.fire({
                html: `<p>The exit code was ${code}</p><p>The exit signal was: ${signal}</p>`,
                showCloseButton: false,
                showCancelButton: false,
                focusConfirm: false
            })
        });
    } catch (error) {
        document.getElementById(`trainbutton`).disabled = false
        Swal.fire({
            html: `<span>${error}</span>`,
            showCloseButton: false,
            showCancelButton: false,
            focusConfirm: false
        })
    }

}

function makeid(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < length; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}