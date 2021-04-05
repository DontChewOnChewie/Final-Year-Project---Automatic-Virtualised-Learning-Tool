const cp = require("child_process");
const fs = require("fs");
let challenge_id, download_btn, run_btn, modal, close_modal_btn;

const setRunButton = () => {
    return fs.existsSync(`Downloads/${challenge_id}`) ? true : false 
}

const showRunModal = () => {
    modal.style.opacity = "1";
    modal.style.zIndex = "100";
}

const closeRunModal = () => {
    modal.style.opacity= "0";
    setTimeout(() => { modal.style.zIndex = "-100"; }, 500);
}

const runLesson = (challenge_id) => {
    download_btn.innerText = "Starting...";
    closeRunModal();

    let start_process = cp.exec(`powershell .\\Downloads\\${challenge_id}\\start.ps1`);

    start_process.stderr.on("data", (data) => { console.error(data); });

    start_process.stdout.on("data", (data) => { console.log(data); });

    start_process.on("close", () => { download_btn.innerText = "Stop"; });  
}

const stopLesson = (challenge_id) => {
    download_btn.innerText = "Stopping...";
    let stop_process = cp.exec(`powershell .\\Downloads\\${challenge_id}\\stop.ps1`);

    stop_process.stderr.on("data", (data) => { console.log(data); });

    stop_process.stdout.on("data", (data) => { console.log(data); });

    stop_process.on("close", () => { download_btn.innerText = "Run..."; });
}

const downloadLesson = (challenge_id) => {
    let download_link = download_btn.getAttribute("href");
    download_btn.innerText = "Downloading...";
    let install_process = cp.exec(`powershell .\\setup_challenge.ps1 ${download_link} "${challenge_id}"`);

    install_process.stderr.on("data", (data) => { console.error(data); });

    install_process.stdout.on("data", (data) => { console.log(data); });

    install_process.on("close", () => { download_btn.innerText = "Run..."; });
}

window.onload = () => {
    run_globals();
    challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];
    download_btn = document.querySelector("footer a" );
    run_btn = document.getElementById("btn-run");
    modal = document.querySelector(".modal");
    close_modal_btn = document.getElementById("close-modal-btn");

    if (setRunButton()) download_btn.innerText = "Run...";

    download_btn.addEventListener("click", (e) =>  {
        e.preventDefault();

        if (download_btn.innerText == "Run...") { 
            showRunModal();
        } else if (download_btn.innerText == "Stop") {
            stopLesson(challenge_id);
        } else {
            downloadLesson(challenge_id)
        }
    });

    run_btn.addEventListener("click", () => { runLesson(challenge_id); });
    close_modal_btn.addEventListener("click", () => { closeRunModal(); });
    modal.addEventListener("click", () => { closeRunModal(); });
}