let {PythonShell} = require('python-shell')
const fs = require("fs")
const readline = require('readline');

var path = require("path")

function start_training(){

    var groupA = document.getElementById("groupa");
    if (groupA.files.length<1){
        var ga = document.getElementById("a_required");
        ga.innerHTML = "Group A folder is required";
        return;
    }
    var groupB = document.getElementById("groupb");
    if (groupB.files.length<1){
        var gb = document.getElementById('b_required');
     gb.innerHTML = "Group B folder is required";
        return;
    }
    var groupaPath = groupA.files[0].path;
    var groupbPath = groupB.files[0].path;
    var gen_name = document.getElementById('generate_name').value;
    var modelname = document.getElementById("modelname").value
    
    var trainArgs = ['train', '-grpA',groupaPath, '-grpB', groupbPath, '-model', modelname, '-gen_name',gen_name]

    var options = {
    mode:'binary',
    scriptPath : __dirname,
    args : trainArgs,
    pythonOptions:['-u'],
    pythonPath: path.join(__dirname,'env/bin/python')

  }
  let pyshell = new PythonShell('app.py', options);

  pyshell.on('message', function(message) {

    console.log(message)
  })
}

