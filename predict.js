var {
    PythonShell
} = require("python-shell");
var path = require('path');
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
    clearGreat() {
        this.groups = {};
    }
}

const store = new Store();


function addGroup(event, clast) {
    const files = event.target.files;
    var folder = files[0].path;
    folder = folder.path;
    store.addGroup(clast, folder)
    document.getElementById(`visible${clast}`).placeholder = folder;
    document.getElementById(`trainbutton`).disabled = false;
    console.log('Saving Directory');
    const options = {
        mode: 'text',
        scriptPath: './server',
        pythonPath: '/usr/local/bin/python3',
        args: ['retrieve_models']
    }
    PythonShell.run('app.py', options, (err, results) => {
        Swal.fire({
            html: `You have ${results}<br/> <input placeholder="Input your model Name"/>>`,
            showCloseButton: true,
            showCancelButton: true,
            focusConfirm: false,
            confirmButtonText: 'Proceed',
            preConfirm: () => {
                return [
                    predict()
                ]
            },
            cancelButtonText: '<i class="fa fa-thumbs-down"></i> Cancel',
        })
    });

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
    console.log('hello')
    document.getElementById('predictprogress').value = 30
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
            document.getElementById(`slides`).hidden = false;
            const slides = document.getElementById(`sliders`);
            //todo: Get the directory for the valid and the count of files in it and loop through below;
            for (let i = 3; i < 8; i++) {
                const img = document.createElement("img");
                img.src = `${folder}`;
                img.className = "mySlides"
                img.style = "width:100%; height:250px;";
                slides.appendChild(img);
            }
            showDivs(5);
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

}