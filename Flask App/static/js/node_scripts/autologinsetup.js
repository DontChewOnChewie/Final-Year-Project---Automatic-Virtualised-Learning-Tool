/* 
    File not currently used, however is the basis for future autologin option.
*/ 

var fs = require("fs");
const remote = require ("electron").remote;

// Function to get a cookie.
function get_cookies() {
    let cookies = document.cookie.split(";");
    let data;
    for (var i=0; i<cookies.length; i++) { 
        let item_key = cookies[i].split("=");
        if (item_key[0].trim() == "data") data = item_key[1].trim();
    }
    return data
}

fs.writeFile("auto_creds", get_cookies(), function (err) {
    if (err) throw err;
});


remote.getCurrentWindow().loadURL("http://localhost:5000/main");