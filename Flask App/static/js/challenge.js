const cp = require("child_process");
let download_btn;

function check_user_has_challenge() {
    let user_challenges = get_cookie("challenges");
    if (user_challenges == undefined) return false;

    let challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];
    user_challenges = user_challenges.split("|");
    for (var i = 0; i < user_challenges.length; i++) {
        if (user_challenges[i] == challenge_id) return true;
    }
    return false;
}

window.onload = function () {
    run_globals();

    download_btn = document.querySelector("footer a" );
    download_btn.addEventListener("click", function (e) {
        e.preventDefault();
        add_challenge_to_user();

        if (!check_user_has_challenge()) {
            let download_link = download_btn.getAttribute("href");
            let challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];
            download_btn.innerText = "Downloading...";
            let install_process = cp.exec(`powershell .\\setup_challenge.ps1 ${download_link} "${challenge_id}"`);

            install_process.stderr.on("data", function (data) {
                console.error(data);
            });

            install_process.stdout.on("data", function (data) {
                console.log(data);
            });

            install_process.on("close", function (code) {
                download_btn.innerText = "Run";
            });
        }
    });

}