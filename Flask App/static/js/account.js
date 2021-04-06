let playBtns, eventHoverLabels, challenges, my_uploads;

const setHoverEventLabel = (target, text) => {
    target.innerText = text;
}

const fadeInChallenge = (target, timeModifier) => {
    setTimeout(() => {
        target.style.opacity = "1";
    }, 700 * timeModifier);
}

const deleteChallenge = (object, challenge_id) => {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4 && xhr.status == 200 && xhr.responseText === "Y") {
            object.style.animation = "delete-item-animation 2s cubic-bezier(0.075, 0.82, 0.165, 1) 0s 1 normal forwards"; 
            setTimeout(() => { object.remove(); }, 2000);
        }
    }

    xhr.open('DELETE', `http://localhost:5000/challenge/${challenge_id}/delete`, true);
    xhr.send(); 
}

const addDeleteOption = (target) => {
    const img = document.createElement("img");
    img.className = "delete-server-button";
    img.src = "/static/images/server.svg";
    img.alt = "Remove Challenge from Server Button";

    const hoverEventSpan = target.parentElement.children[target.parentElement.children.length - 1];
    img.onmouseover = () => { hoverEventSpan.innerText = "Remove Challenge from Server"; }
    img.onmouseout = () => { hoverEventSpan.innerText = "Challenge Options"; }
    const challengeParent = target.parentElement.parentElement.parentElement;
    img.onclick = () => { deleteChallenge(challengeParent, target.getAttribute("data-id")); }

    target.insertBefore(img, target.children[0]);
}

window.onload = function () {
    run_globals();
    get_user_downloaded_challenges(document.getElementById("my-list"));

    playBtns = document.getElementsByClassName("play-button");
    eventHoverLabels = document.getElementsByClassName("hover-event");
    challenges = document.getElementsByClassName("challenge");
    my_uploads = document.querySelectorAll("#my-uploads .challenge-options-wrapper div");

    for (let i = 0; i < playBtns.length; i++) {
        playBtns[i].addEventListener("mouseover", () => setHoverEventLabel(eventHoverLabels[i], "Go to Challenge"));
        playBtns[i].addEventListener("mouseout", () => setHoverEventLabel(eventHoverLabels[i], "Challenge Options"));
    }

    for (let i = 0; i < my_uploads.length; i++) {
        addDeleteOption(my_uploads[i]);
    }

    for (let i = 0; i < challenges.length; i++) { 
        fadeInChallenge(challenges[i], i); 
    }
}