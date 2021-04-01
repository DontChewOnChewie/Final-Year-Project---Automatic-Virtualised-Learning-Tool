const {app, BrowserWindow} = require('electron');
const fs = require('fs');
const internetAvailable = require('internet-available');

const config_defaults = {
    "installed":0,
    "default_machine":"Project_Kali",
    "selected_machine":"Project_Kali"
}

const createFiles = () => {
    if (!fs.existsSync("./Downloads")) {
        fs.mkdir("./Downloads", (err) => {
            if (err) throw err;
        });
    }

    if (!fs.existsSync("./VM_Shared")) {
        fs.mkdir("./VM_Shared", (err) => {
            if (err) throw err;
        })
    }

    if (!fs.existsSync("config.json")) {
        fs.writeFile("config.json", JSON.stringify(config_defaults, null, 4), function (err) {
            if (err) throw err;
        });
    }
}

const createWindow = () => {
    const mainWindow = new BrowserWindow({
        frame: false,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
        }
    });

    createFiles();

    internetAvailable().then(function(){
        mainWindow.webContents.session.clearCache( function() { /*Clear Cache for debugging.*/ }) ;
        if (fs.existsSync("auto_creds")) {
            fs.readFile('auto_creds', 'utf8', function (err, data) {
                if (err) return console.log(err);
                mainWindow.loadURL("http://localhost:5000/autologin?data=" + data);
            });
        }
        else {
            fs.readFile("config.json", 'utf8', function (err, data) {
                const installed = JSON.parse(data).installed;
                installed === 1 ? mainWindow.loadURL("http://localhost:5000/login") : mainWindow.loadURL("http://localhost:5000/");
            });
        }
    }).catch(function(){
        mainWindow.loadFile("./OfflineMode/index.html");
    });
    
    mainWindow.maximize();
}

app.on('ready', createWindow);