const cp = require("child_process");
const fs = require("fs");
let download_btn;

function set_run_button() {
    let challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];
    return fs.existsSync(`Downloads/${challenge_id}`) ? true : false 
}

window.onload = function () {
    run_globals();

    download_btn = document.querySelector("footer a" );
    if (set_run_button()) download_btn.innerText = "Run...";

    download_btn.addEventListener("click", function (e) {
        let challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];
        e.preventDefault();

        if (download_btn.innerText == "Run...") {
            download_btn.innerText = "Starting...";
            let start_process = cp.exec(`powershell .\\Downloads\\${challenge_id}\\start.ps1`);

            start_process.stderr.on("data", function (data) {
                console.error(data);
            });

            start_process.stdout.on("data", function (data) {
                console.log(data);
            });

            start_process.on("close", function () {
                download_btn.innerText = "Stop";
            });

        } else if (download_btn.innerText == "Stop") {
            download_btn.innerText = "Stopping...";
            let stop_process = cp.exec(`powershell .\\Downloads\\${challenge_id}\\stop.ps1`);

            stop_process.stderr.on("data", function (data) {
                console.log(data);
            });

            stop_process.stdout.on("data", function (data) {
                console.log(data);
            });

            stop_process.on("close", function () {
                download_btn.innerText = "Run..."
            });
        } else {
            let download_link = download_btn.getAttribute("href");
            download_btn.innerText = "Downloading...";
            let install_process = cp.exec(`powershell .\\setup_challenge.ps1 ${download_link} "${challenge_id}"`);

            install_process.stderr.on("data", function (data) {
                console.error(data);
            });

            install_process.stdout.on("data", function (data) {
                console.log(data);
            });

            install_process.on("close", function (code) {
                download_btn.innerText = "Run...";
            });
        }
    });

}