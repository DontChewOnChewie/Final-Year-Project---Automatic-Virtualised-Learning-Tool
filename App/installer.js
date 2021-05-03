/*
    File called when user has finished downloading the first install stage.
*/

const fs = require("fs");


// Function used to set the installed value in config file to 1.
const setInstalled = () => {
    if (fs.existsSync(`${__dirname}\\config.json`)) {
        fs.readFile(`${__dirname}\\config.json`, 'utf8', (err, data) => {
            if (err) return console.log(err);

            const json_data = JSON.parse(data);
            json_data.installed = 1;
            console.log("Json Data changed to 1.");

            fs.writeFileSync(`${__dirname}\\config.json`, JSON.stringify(json_data, null, 4), (err) => {
                if (err) throw err;
            });
        });
    }
};

setInstalled();