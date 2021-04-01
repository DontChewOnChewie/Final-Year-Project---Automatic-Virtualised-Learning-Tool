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

        const span = document.createElement("span");
        span.className = challenge.difficulty.toLowerCase();
        span.innerText = challenge.difficulty;

        const title = document.createElement("h3");
        title.innerText = challenge.name;
        title.appendChild(span);

        const imageWrapper = document.createElement("div");
        imageWrapper.className = "image-wrapper";

        const img = document.createElement("img");
        img.alt = "Challenge Icon";
        if (challenge.banner_path != null && challenge.banner_path != undefined && challenge.banner_path != "") img.src = challenge.banner_path;
        else img.src = "/static/images/placeholder.jpg";

        const hoverEventSpan = document.createElement("span");
        hoverEventSpan.className = "hover-event";
        hoverEventSpan.innerText = "Challenge Options";

        const delServerBtn = document.createElement("img");
        delServerBtn.src = "/static/images/server.svg";
        delServerBtn.className = "delete-server-button";
        delServerBtn.onmouseover = () => { hoverEventSpan.innerText = "Remove Challenge from Server" }
        delServerBtn.onmouseout = () => { hoverEventSpan.innerText = "Challenge Options" }

        const delPCBtn = document.createElement("img");
        delPCBtn.src = "/static/images/pc.svg";
        delPCBtn.className = "delete-pc-button";
        delPCBtn.onmouseover = () => { hoverEventSpan.innerText = "Remove Challenge from PC" }
        delPCBtn.onmouseout = () => { hoverEventSpan.innerText = "Challenge Options" }

        const playBtn = document.createElement("img");
        playBtn.src = "/static/images/play.svg";
        playBtn.className = "play-button";
        playBtn.onclick = () => { navigate_to_challenge(challenge.id) }
        playBtn.onmouseover = () => { hoverEventSpan.innerText = "Go to Challenge" }
        playBtn.onmouseout = () => { hoverEventSpan.innerText = "Challenge Options" }

        const buttonWrapper = document.createElement("div");
        buttonWrapper.appendChild(delServerBtn);
        buttonWrapper.appendChild(delPCBtn);
        buttonWrapper.appendChild(playBtn);

        const imageOpacityOverlay = document.createElement("div");
        imageOpacityOverlay.className = "challenge-options-wrapper";
        imageOpacityOverlay.appendChild(buttonWrapper);
        imageOpacityOverlay.appendChild(hoverEventSpan);

        imageWrapper.appendChild(img);
        imageWrapper.appendChild(imageOpacityOverlay);
        wrapper.appendChild(title);
        wrapper.appendChild(imageWrapper);
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