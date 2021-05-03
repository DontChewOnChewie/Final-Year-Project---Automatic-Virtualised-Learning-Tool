/* 
    File used to manage the settings page.
*/

const cp = require('child_process');
const fs = require('fs');
let dd_machines, btn_save;

// Function used to save the users settings changes to the config file.
const saveChanges = () => {
    if (fs.existsSync("config.json")) {
        fs.readFile('config.json', 'utf8', (err, data) => {
            if (err) return console.log(err);

            const json_data = JSON.parse(data);
            json_data.selected_machine = dd_machines.value;

            fs.writeFile("config.json", JSON.stringify(json_data, null, 4), (err) => {
                if (err) throw err;
            });
        });
    }
}

// Function used to add all Virtual Machines available to the drop down list.
const populateVMDropDown = () => {
    const machines = [];
    const process = cp.exec("VBoxManage list vms");

    process.stdout.on("data", (data) => {
        data.split("\n").forEach(element => {
            const machine_name = element.split('"')[1];
            if (machine_name != undefined) machines.push(machine_name);
        });
    });
    

    setTimeout(() => {
        machines.forEach(element => {
            const option = document.createElement("option");
            option.innerText = element;
            dd_machines.appendChild(option);
        });
    }, 2000);
}

window.onload = () => {
    run_globals();
    dd_machines = document.getElementsByTagName("select")[0];
    btn_save = document.querySelector("footer");
    btn_save.addEventListener("click", () => { saveChanges(); });
    populateVMDropDown();
}