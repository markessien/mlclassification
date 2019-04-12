
let {PythonShell} = require('python-shell');
const fs = require("fs");
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
    mode:'text',
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

function start_prediction(){
    var folder = document.getElementById('predfolder');
    var fileselected = document.getElementById('predfile');
    if (folder.files.length>0){
        var working = document.getElementById("working");
        working.innerHTML = "Predicting folder,...just a few minutes";
        var folderpath = folder.files[0].path;
        var predArgs = ['predict', '--path',folderpath];

    var options = {
    mode:'text',
    scriptPath : __dirname,
    args : predArgs,
    pythonOptions:['-u'],
    pythonPath: path.join(__dirname,'env/bin/python')

  };

  let pyshell = new PythonShell('app.py', options);

  pyshell.on('message', function(message) {

    var working = document.getElementById("working");
    working.innerHTML = message;
  })
  pyshell.end(function (err,code,signal) {
  if (err) throw err;
  
});
    }
  else if (fileselected.files.length>0){
    var working = document.getElementById("working");
        working.innerHTML = "Predicting image ...";
        var filepath = fileselected.files[0].path;
        var predArgs = ['predict', '--path',filepath];

    var options = {
    mode:'text',
    scriptPath : __dirname,
    args : predArgs,
    pythonOptions:['-u'],
    pythonPath: path.join(__dirname,'env/bin/python')

  };

  let pyshell = new PythonShell('app.py', options);

  pyshell.on('message', function(message) {

    var working = document.getElementById("working");
    working.innerHTML = message;
  })

}
}

function allmodels(){
    var options = {
    mode:'text',
    scriptPath : __dirname,
    args : ['retrieve_models'],
    pythonOptions:['-u'],
    pythonPath: path.join(__dirname,'env/bin/python')

  };
  let pyshell = new PythonShell('app.py', options);
  pyshell.on("message",function(){

  });

}

