const cp = require("child_process");
let btn_vbox, btn_docker, btn_both;
let main, btn_skip, status_label;
let dependancies;

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
        btn_skip.style.backgroundColor = "#333d61";
        btn_skip.innerText = "Skip to Sign Up or Sign In >>";
        btn_skip.setAttribute("href", "/login");

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
    btn_skip.removeAttribute("href");
    btn_skip.style.backgroundColor = "#aa3131";
    btn_skip.innerText = "Cannot move on until installs are complete.";

    for (var i = 0 ; i < dependancies.length; i++) {
        console.log(dependancies[i]);
        dependancies[i].removeChild(dependancies[i].children[1]); // Remove Buttons
        dependancies[i].children[0].className = args[i] == 1 ? "install pulsing-install" : "install no-install";
    }
}

window.onload = function () {
    run_globals();

    btn_vbox = document.getElementById("btn-vbox");
    btn_docker = document.getElementById("btn-docker");
    btn_both = document.getElementById("btn-both");
    main = document.getElementsByTagName("main")[0];
    btn_skip = document.querySelector("footer a");
    dependancies = document.querySelectorAll(".dependancy");

    btn_vbox.addEventListener("click", function() { start_installs([1, 0]); });
    btn_docker.addEventListener("click", function() { start_installs([0, 1]); });
    btn_both.addEventListener("click", function() { start_installs([1, 1]); });
};