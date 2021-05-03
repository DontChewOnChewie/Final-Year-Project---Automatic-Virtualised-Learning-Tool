/* 
    File used to manage global functions used by a lot of pages.
*/

const remote = require("electron").remote
let btn_close, btn_minimise;
let account_link;
let toolbar_icons, tooltip, tooltip_span;

// Function used to get the value of a given cookie name.
const get_cookie = (cookie_name) => {
    const cookies = document.cookie.split(";")
    for (var i = 0; i < cookies.length; i++) {
        const cookie_dict = cookies[i].split("=")
        if (cookie_dict[0].trim() == cookie_name) return cookie_dict[1];
    }
}

// Function used to setup the link to a users page.
const setup_links = () => {
    var username = get_cookie("user");
    if (username === undefined) account_link.href = "/login";
    else account_link.href = `/account/${username}`;
}

// Function used to set the link of a challenge object.
const navigate_to_challenge = (id) => {
    window.location.href = `/challenge/${id}`;
}

// Function used to display tooltip of header option.
const displayTooltip = (e, target) => {
    const tooltip_value = target.getAttribute("data-tooltip");
    tooltip.style.top = `${e.clientY + 10}px`;
    tooltip.style.left = `${e.clientX + 10}px`;
    tooltip_span.innerText = tooltip_value;
}

// Function used to hide tooltip when header option is not being hovered.
const hideTooltip = () => {
    tooltip.style.top = "1000px";
    tooltip.style.left = "0px";
    tooltip_span.innerText = ""; 
}

// Function used to setup all buttons and functionality that is globally used.
// This includes setting up the close and minimise button.
const run_globals = () => {
    account_link = document.getElementById("account-link");
    btn_close = document.getElementById("btn_close");
    btn_minimise = document.getElementById("btn_minimise");
    toolbar_icons = document.getElementsByClassName("toolbar-icon");
    tooltip = document.getElementById("tooltip");
    tooltip_span = document.querySelector("#tooltip span");

    for (let i = 0; i < toolbar_icons.length;  i++) {
        toolbar_icons[i].addEventListener("mouseover", (e) => { displayTooltip(e, toolbar_icons[i]); });
        toolbar_icons[i].addEventListener("mouseout", () => { hideTooltip(); });
    }
    
    btn_close.addEventListener("click", () => { remote.getCurrentWindow().close(); });
    btn_minimise.addEventListener("click", () => { remote.getCurrentWindow().minimize(); });
    if (account_link != null) setup_links();
}