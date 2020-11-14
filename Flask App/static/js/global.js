let account_link;

function get_cookie(cookie_name) {
    let cookies = document.cookie.split(";")
    for (var i = 0; i < cookies.length; i++) {
        let cookie_dict = cookies[i].split("=")
        if (cookie_dict[0] == cookie_name) return cookie_dict[1];
    }
}

function run_globals() {
    account_link = document.getElementById("account-link")
    account_link.href = `account/${get_cookie("user")}`;
}