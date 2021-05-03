/*
    File used to manage the users installing of the program.
*/

const cp = require("child_process");
const fs = require("fs");
let btn_both, main, dependancies, btn_installed;

// Run the installer confirmation.
const setInstalledConfig = () => {
    cp.exec("node installer.js");
}

// Function used to start the install process on button click.
const startInstall = (args) => {
    let final_args = [".\\installs.ps1"];
    for (var i = 0; i < args.length; i++) {
        final_args.push(args[i]);
    } 

    setupInstallingView();

    let install_process = cp.spawn("powershell", final_args);

    install_process.stdout.on("data", (data) => { console.log(data); });

    install_process.stderr.on("data", (data) => { console.log(data); });
}

// Function used to setup what the user sees whilst program is installing.
const setupInstallingView = () => {
    main.removeChild(document.querySelector(".installed"));  
    btn_both.innerText = "Installing...";
}

// Function used to check if the program has finished installing.
const checkInstalled = () => {
     if (fs.existsSync("installed.dat")) {
         fs.unlinkSync("installed.dat");
         btn_both.innerText = "Installed, Restart Your PC";
         btn_both.disabled = true;
     }
}

window.onload = () => {
    run_globals();

    btn_both = document.getElementById("btn-both");
    main = document.getElementsByTagName("main")[0];
    dependancies = document.querySelectorAll(".dependancy");
    btn_installed = document.getElementById("already-installed");

    btn_installed.addEventListener("click", () => { setInstalledConfig(); })
    btn_both.addEventListener("click", () => { startInstall([1, 1, process.cwd()]); });
    setInterval(() => {
        checkInstalled();
    }, 1000);
};