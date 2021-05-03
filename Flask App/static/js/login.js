/* 
    File used to manage the login/signup page.
*/

const cp = require("child_process");
const fs = require("fs");
let toggle_pass_button, password_field;

// Function used to toggle whether or not the password field is visible to the user.
const togglePasswordButton = () => {
    var toggled = toggle_pass_button.getAttribute("data-enabled");
    if (toggled === "0") {
        toggle_pass_button.setAttribute("data-enabled", "1");
        toggle_pass_button.src = "/static/images/eye.svg";
        password_field.type = "text";
    } else {
        toggle_pass_button.setAttribute("data-enabled", "0");
        toggle_pass_button.src = "/static/images/eye-off.svg";
        password_field.type = "password";
    }
}

// Function used to check if the network installer needs to be ran.
const checkNetworkSetup = async () => {
    if (fs.existsSync("config.json")) {
        fs.readFile('config.json', 'utf8', (err, data) => {
            if (err) return console.log(err);
            let json = JSON.parse(data);
            console.log(json);
            if (json.installed === 1) {
                json.installed = 2;
                fs.writeFileSync("config.json", JSON.stringify(json, null, 4), (err) => {
                    if (err) throw err;
                });

                const args = [".\\setup_networks.ps1", process.cwd()];

                let install_process = cp.spawn("powershell", args);

                install_process.stdout.on("data", (data) => { console.log(data); });
            
                install_process.stderr.on("data", (data) => { console.log(data); });
            }
        });
    }
}

window.onload = () => {
    run_globals();
    checkNetworkSetup();
    toggle_pass_button = document.getElementById("toggle-password");
    password_field = document.querySelector("input[type='password']");
    toggle_pass_button.addEventListener("click", () => { togglePasswordButton(); });
}