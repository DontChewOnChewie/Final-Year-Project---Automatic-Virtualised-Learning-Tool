/* 
    File used to manage the mauanl install page.
*/

const cp = require("child_process");
let btn_network_install;

window.onload = () => {
    run_globals();

    btn_network_install = document.querySelector("button");
    btn_network_install.addEventListener("click", () => {
        window.location.href="/login";
    });
}