const fs = require('fs');
const { disconnect } = require('process');

let user = get_cookie("user");

function write_new_user(full_json) {
    let updated_json = full_json;
    updated_json.users[user] = [];
    fs.writeFile('config.json', JSON.stringify(updated_json, null, 4), function (err) {
        if (err) throw err;
    }); 
}

function add_new_user_to_config() {
    fs.readFile('config.json', 'utf8', function (err, data) {
        if (err) return console.log(err);
        if (user == undefined) return;

        let json_data = JSON.parse(data);
        let users = Object.keys(json_data.users);

        for (var i = 0; i < users.length; i++) {
            if (users[i] == user) return;
        }
        write_new_user(json_data);
    });  
}

function add_challenge_to_system(system_challenges, challenge_id) {
    for (var i = 0; i < system_challenges.length; i++) {
        if (challenge_id == system_challenges[i]) return false;
    }
    return true;
}

function write_challenge_to_user(full_json, challenge_id) {
    let updated_json = full_json;
    updated_json.users[user].push(parseInt(challenge_id));
    let add_to_system = add_challenge_to_system(full_json.challenges, challenge_id);
    if (add_to_system) updated_json.challenges.push(challenge_id);
    fs.writeFile('config.json', JSON.stringify(updated_json, null, 4), function (err) {
        if (err) throw err;
    });
    return add_to_system; 
}

function add_challenge_to_user() {
    fs.readFile('config.json', 'utf8', function (err, data) {
        if (err) return console.log(err);
        if (user == undefined) user = "";
        let json_data = JSON.parse(data);
        let _user = json_data.users[user];
        let challenge_id = document.location.href.split("/")[document.location.href.split("/").length -1];

        for (var i = 0; i < _user.length; i++) {
            if (_user[i] == parseInt(challenge_id)) return false;
        }
        return write_challenge_to_user(json_data, parseInt(challenge_id));
    });  
}

function get_challenges_for_user() {
    fs.readFile('config.json', 'utf8', function (err, data) {
        if (err) return console.log(err);
        if (user == undefined) return;

        let json_data = JSON.parse(data);
        if (user == undefined) user = "";
        let challenge_list = json_data.users[user];
        document.location.href = `/main?list=${challenge_list}`;
    }); 
}

switch (document.location.pathname.split("/")[1]) {
    case "login":
    case "autologin":
    case "autologinsetup":
        add_new_user_to_config();
        get_challenges_for_user();
        break;
}





 