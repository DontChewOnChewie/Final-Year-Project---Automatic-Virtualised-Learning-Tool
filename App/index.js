const {app, BrowserWindow} = require('electron');
const fs = require('fs');
const internetAvailable = require('internet-available');

const config_defaults = {
    "installed":0,
    "default_machine":"Project_Kali",
    "selected_machine":"Project_Kali",
    "nat_network_name":"Project_NAT_Net"
}

// Function used to create all files needed for program to run.
const createFiles = async () => {
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

// Function used to create the loading bootstraper window.
const createBootstrapperWindow = () => {
    const bootstrapWindow = new BrowserWindow({
        frame: false,
        width: 120,
        height: 150,
        center: true,
        resizable: false,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
        }
    });
    bootstrapWindow.loadFile("./Bootstrapper/Bootstrapper.html");
    return bootstrapWindow;
}

// Function used to create the main window.
const createWindow = () => {
    const mainWindow = new BrowserWindow({
        frame: false,
        show: false,
        webPreferences: {
            nodeIntegration: true,
            enableRemoteModule: true,
        }
    });

    // Check if the user has internet connectivity available.
    // If not then load offline mode.
    internetAvailable().then( () => {
        mainWindow.webContents.session.clearCache( () => { /*Clear Cache for debugging.*/ }) ;
        if (fs.existsSync("auto_creds")) {
            fs.readFile('auto_creds', 'utf8', (err, data) => {
                if (err) return console.log(err);
                mainWindow.loadURL("http://localhost:5000/autologin?data=" + data);
            });
        }
        else {
            fs.readFile("config.json", 'utf8', (err, data) => {
                const installed = JSON.parse(data).installed;
                installed > 0 ? mainWindow.loadURL("http://localhost:5000/login") : mainWindow.loadURL("http://localhost:5000/");
            });
        }
    }).catch( () => {
        mainWindow.loadFile("./OfflineMode/index.html");
    });
    
    mainWindow.maximize();
}

app.on('ready', () => {
    createWindow();
    setTimeout(() => {
        const bootstrapWindow = createBootstrapperWindow();
        setTimeout(() => { bootstrapWindow.close(); }, 2000);
    }, 100);
    createFiles();
});