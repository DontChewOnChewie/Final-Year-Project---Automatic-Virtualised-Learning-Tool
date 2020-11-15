let username_btn, email_btn, password_btn, btn_container;
let new_detail_inp, conf_detail_inp;

function change_input_info(tag) {
    new_detail_inp.placeholder = `New ${tag}...`;
    conf_detail_inp.placeholder = `Confirm New ${tag}...`;
    
    switch (tag) {
        case "Username":
            new_detail_inp.type = "text";
            new_detail_inp.name = "username";
            conf_detail_inp.type = "text";
            conf_detail_inp.name = "conf_username";
            break;
        case "Email":
            new_detail_inp.type = "email";
            new_detail_inp.name = "email";
            conf_detail_inp.type = "email";
            conf_detail_inp.name = "conf_email";
            break;
        case "Password":
            new_detail_inp.type = "password";
            new_detail_inp.name = "password";
            conf_detail_inp.type = "password";
            conf_detail_inp.name = "conf_password";
            break;
    }
}

function set_selected_button(btn) {
    let selected = document.querySelector(".selected");
    if (selected == btn) return;

    selected.className = "";
    btn.className = "selected";
    change_input_info(btn.innerText);
}

window.onload = function() {
    run_globals();

    username_btn = document.getElementById("username-edit-btn")
    email_btn = document.getElementById("email-edit-btn");
    password_btn = document.getElementById("password-edit-btn");
    btn_container = username_btn.parentElement;

    for (var i = 0; i < btn_container.children.length; i++) {
        btn_container.children[i].addEventListener("click", function () { set_selected_button(this); })
    }

    new_detail_inp = document.getElementById("new-detail");
    conf_detail_inp = document.getElementById("conf-new-detail");
}