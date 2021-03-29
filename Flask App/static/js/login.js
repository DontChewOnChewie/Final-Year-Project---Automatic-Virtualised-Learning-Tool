let toggle_pass_button, password_field;

function toggle_password_button() {
    var toggled = toggle_pass_button.getAttribute("data-enabled");
    console.log(toggled);
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

window.onload = function () {
    run_globals();
    toggle_pass_button = document.getElementById("toggle-password");
    password_field = document.querySelector("input[type='password']");
    toggle_pass_button.addEventListener("click", function () { toggle_password_button(); });
}