let account_link;

function get_cookie(cookie_name) {
    let cookies = document.cookie.split(";")
    for (var i = 0; i < cookies.length; i++) {
        let cookie_dict = cookies[i].split("=")
        if (cookie_dict[0].trim() == cookie_name) return cookie_dict[1];
    }
}

function setup_links() {
    console.log(get_cookie("user"));
    account_link_value = `account/${get_cookie("user")}`;
    account_link.href = account_link_value != null ? account_link_value : "login";
}

function run_globals() {
    account_link = document.getElementById("account-link");
    setup_links();
}