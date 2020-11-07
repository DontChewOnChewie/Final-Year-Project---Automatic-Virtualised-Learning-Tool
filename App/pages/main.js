const remote = require('electron').remote;
const app = remote.app;

const closeBtn = document.getElementById("close");
closeBtn.onclick = closeWindow;

const minimizeBtn = document.getElementById("minimize");
minimizeBtn.onclick = minimizeWindow;

function closeWindow () { app.exit(); }

function minimizeWindow () { remote.BrowserWindow.getFocusedWindow().minimize(); }