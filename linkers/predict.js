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
    const files = event.target.files;
    var folder = files[0];
    folder = folder.webkitRelativePath;
    store.addGroup(clast, folder)
    document.getElementById(`visible${clast}`).placeholder = folder;
    document.getElementById(`trainbutton`).disabled = false;
    console.log('Saving Directory')
    Swal.fire({
        html: `You can use <b>${JSON.stringify(store.getGroup())}</b>`,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: 'Proceed',
        preConfirm: () => {
            return [
                train()
            ]
        },
        cancelButtonText: '<i class="fa fa-thumbs-down"></i> Cancel',
    })
    console.log('Saved Directory')
}

function addPredict(event) {
    const files = event.target.files;
    var folder = files[0];
    folder = folder.webkitRelativePath;
    store.addPredict(folder)
    document.getElementById(`predictinput`).placeholder = folder;
    // document.getElementById(`predictbutton`).disabled = false;
    Swal.fire({
        html: `You can use <b>${ path.join(__dirname, folder)}</b>`,
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
    console.log('Saved Directory')
}

function train() {
    console.log('train');
}

function predict() {
    console.log('hello')
    document.getElementById('predictprogress').value = 30
    var options = {
        scriptPath: path.join(__dirname, '/../server'),
        pythonPath: '/usr/local/bin/python3',
        args: ['predict', '-path', 'testimages/nh3.jpg']
    }
    try {

        const predict = new PythonShell('app.py', options);
        predict.end((err, code, message) => {
            const perc = 100;
            document.getElementById('predictprogress').value = perc;
            document.getElementById('predicttag').innerText = `${perc}%`;
            document.getElementById('predictresult').innerText = 'Completed';
            document.getElementById(`slides`).hidden = false;
            const slides = document.getElementById(`sliders`);
            for (let i = 3; i < 8; i++) {
                const img = document.createElement("img");
                img.src = `./testimages/nh${i}.jpg`;
                img.className = "mySlides"
                img.style = "width:100%; height:250px;";
                slides.appendChild(img);
            }
            showDivs(5)
        })
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