const remote = require("electron").remote;
const fs = require("fs");
const cp = require("child_process");
let closeBtn, minimiseBtn, carousel;

const create_challenge_divs = () => {
    fs.readdir("./Downloads/", (err, files) => {
        //handling error
        if (err) return console.log('Unable to scan directory: ' + err); 
        
        files.forEach((file) => {
            const container = document.createElement("div");
            container.className = "challenge";
    
            const title = document.createElement("h3");
            title.innerText = file;
    
            const startBtn = document.createElement("button");
            startBtn.type = "button";
            startBtn.innerText = "Run...";
            startBtn.setAttribute("data-running", 0);
            startBtn.addEventListener("click", (e) => {
                const self = e.target;
                const running = self.getAttribute("data-running");
                console.log(running);

                if (running == 0) {
                    cp.exec(`powershell .\\Downloads\\${file}\\start.ps1`);
                    self.setAttribute("data-running", 1);
                    self.innerText = "Stop...";
                } else {
                    cp.exec(`powershell .\\Downloads\\${file}\\stop.ps1`);
                    self.setAttribute("data-running", 0);
                    self.innerText = "Run...";
                }
            });
    
            container.appendChild(title);
            container.appendChild(startBtn);
            carousel.appendChild(container);
        }); 
    });
}

window.onload = () => {
    carousel = document.getElementById("my-list");
    create_challenge_divs();

    closeBtn = document.getElementById("btn_close");
    closeBtn.addEventListener("click", () => { remote.getCurrentWindow().close(); });

    minimiseBtn = document.getElementById("btn_minimise");
    minimiseBtn.addEventListener("click", () => { remote.getCurrentWindow().minimize(); });
}