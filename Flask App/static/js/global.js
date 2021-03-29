const remote = require("electron").remote
let btn_close, btn_minimise;
let account_link;

function get_cookie(cookie_name) {
    let cookies = document.cookie.split(";")
    for (var i = 0; i < cookies.length; i++) {
        let cookie_dict = cookies[i].split("=")
        if (cookie_dict[0].trim() == cookie_name) return cookie_dict[1];
    }
}

function setup_links() {
    var username = get_cookie("user");
    if (username === undefined) {
        account_link.href = "/login";
        account_link.innerText = "Login/Sign Up";
    } else {
        account_link.href = `/account/${username}`;
    }
}

function navigate_to_challenge(id) {
    window.location.href = `/challenge/${id}`;
}

function run_globals() {
    account_link = document.getElementById("account-link");
    btn_close = document.getElementById("btn_close");
    btn_minimise = document.getElementById("btn_minimise");
    
    btn_close.addEventListener("click", function() { remote.getCurrentWindow().close(); });
    btn_minimise.addEventListener("click", function() { remote.getCurrentWindow().minimize(); });
    if (account_link != null) setup_links();
}