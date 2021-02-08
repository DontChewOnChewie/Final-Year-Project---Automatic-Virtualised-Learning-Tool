const fs = require('fs');

const create_challenge_divs = (target, json) => {
    const challenge_json = JSON.parse(json);
    if (Object.keys(challenge_json).length == 0) {
        const title = document.createElement("h3");
        title.innerText = "No Downloads";
        title.style.textAlign = "center";
        target.appendChild(title);
    }

    Object.keys(challenge_json).forEach(key => {
        const challenge = JSON.parse(challenge_json[key]);
        console.log(challenge);

        const wrapper = document.createElement("div");
        wrapper.className = "challenge";
        wrapper.onclick = () => { navigate_to_challenge(challenge.id) }

        const span = document.createElement("span");
        span.className = challenge.difficulty.toLowerCase();
        span.innerText = challenge.difficulty;

        const title = document.createElement("h3");
        title.innerText = challenge.name;
        title.appendChild(span);

        const img = document.createElement("img");
        img.alt = "Challenge Icon";
        if (challenge.banner_path != null && challenge.banner_path != undefined && challenge.banner_path != "") img.src = challenge.banner_path;
        else img.src = "/static/images/placeholder.jpg";

        wrapper.appendChild(title);
        wrapper.appendChild(img);
        target.appendChild(wrapper);
    });
    
}

const get_user_downloaded_challenges = async (target) => {
    if (fs.existsSync("./Downloads")) {
        fs.readdir("./Downloads", (err, files) => {
            if (err) { throw err; }
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if(xhr.readyState == 4 && xhr.status == 200) {
                    create_challenge_divs(target, xhr.responseText);
                }
            }

            xhr.open('GET', `http://localhost:5000/challenge/getuserchallengedata?obj=${files}`, true);
            xhr.send();
        });
    }
}