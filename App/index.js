const {app, BrowserWindow} = require('electron');
const path = require('path');

const createWindow = () => {
    const mainWindow = new BrowserWindow({
        frame: false,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
        }
    });

    mainWindow.loadURL("http://localhost:5000/");
    mainWindow.maximize();
}

app.on('ready', createWindow);