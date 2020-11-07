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

    mainWindow.loadFile(path.join(__dirname, '/pages/index.html')); 
    mainWindow.maximize();
}

app.on('ready', createWindow);