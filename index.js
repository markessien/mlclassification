 // Code for electron dialog
 const {
     dialog
 } = require('electron').remote;

 const {
     ipcRenderer
 } = require('electron')

 ipcRenderer.on('trainingDatasets', (event, args) => {
     console.log(args)
     var datasets = document.getElementById("trainingDatasets")
     clearAndAppend(datasets, args)
 })

 ipcRenderer.on('testDatasets', (event, args) => {
     var datasets = document.getElementById("testDatasets")
     clearAndAppend(datasets, args)
 })

 function clearAndAppend(datasets, datasetEntries) {
     while (datasets.firstChild) {
         datasets.removeChild(datasets.firstChild);
     }

     datasetEntries.forEach(element => {
         datasets.innerHTML += (`<li>${element}</li>`)
     });
 }

 function getDataset(eventName) {
     console.log(eventName)
     console.log("showing")
     var path = dialog.showOpenDialog({
         properties: ['openDirectory']
     });
     if (path != null) {
         ipcRenderer.send(eventName, path)
     }
 }

 function showDialog() {
     console.log("showing")
     var path = dialog.showOpenDialog({
         properties: ['openDirectory']
     });
     ipcRenderer.send('datasetRecovery', path)
 }



 // the image slider
 