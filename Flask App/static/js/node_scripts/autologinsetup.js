var fs = require("fs");
const remote = require ("electron").remote;

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