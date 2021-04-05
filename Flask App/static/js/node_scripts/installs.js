const cp = require("child_process");
const fs = require("fs");
let btn_both, btn_installed;
let main, status_label;
let dependancies;

const setInstalled = () => {
    if (fs.existsSync("config.json")) {
        fs.readFile('config.json', 'utf8', (err, data) => {
            if (err) return console.log(err);

            const json_data = JSON.parse(data);
            json_data.installed = 1;

            fs.writeFile("config.json", JSON.stringify(json_data, null, 4), (err) => {
                if (err) throw err;
            });
        });
    }
};

function start_installs(args) {
    let final_args = [".\\installs.ps1"];
    for (var i = 0; i < args.length; i++) {
        final_args.push(args[i]);
    } 

    setup_installing_view(args);

    let install_process = cp.spawn("powershell", final_args);

    install_process.stdout.on("data", function (data) {
        status_label.innerText = data;
    });

    install_process.on("close", function (code) {

        for (var i = 0; i < dependancies.length; i++) {
            if (args[i] == 1) dependancies[i].children[0].className ="install finish-install";
        }

    });
}

function setup_installing_view(args) {
    status_label = document.createElement("h3");
    status_label.className = "status-label";
    
    main.removeChild(btn_both);
    main.appendChild(status_label);

    for (var i = 0 ; i < dependancies.length; i++) {
        console.log(dependancies[i]);
        dependancies[i].removeChild(dependancies[i].children[1]); // Remove Buttons
        dependancies[i].children[0].className = args[i] == 1 ? "install pulsing-install" : "install no-install";
    }
}

window.onload = function () {
    run_globals();

    btn_both = document.getElementById("btn-both");
    btn_installed = document.querySelector(".installed a");
    main = document.getElementsByTagName("main")[0];
    dependancies = document.querySelectorAll(".dependancy");

    btn_both.addEventListener("click", function() { start_installs([1, 1]); });
    btn_installed.addEventListener("click", () => { setInstalled(); });
};