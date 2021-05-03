/* 
    File used to manage the main page.
*/ 

let playBtns, eventHoverLabels, challenges;

// Function used to set the label over a challenge object on hover.
const setHoverEventLabel = (target, text) => {
    target.innerText = text;
}

// Function used to fade in a challenge based on a timed event.
const fadeInChallenge = (target, timeModifier) => {
    setTimeout(() => {
        target.style.opacity = "1";
    }, 700 * timeModifier);
}

window.onload = function () {
    run_globals();
    get_user_downloaded_challenges(document.getElementById("my-list"));

    playBtns = document.getElementsByClassName("play-button");
    eventHoverLabels = document.getElementsByClassName("hover-event");
    challenges = document.getElementsByClassName("challenge");

    for (let i = 0; i < playBtns.length; i++) {
        playBtns[i].addEventListener("mouseover", () => setHoverEventLabel(eventHoverLabels[i], "Go to Challenge"));
        playBtns[i].addEventListener("mouseout", () => setHoverEventLabel(eventHoverLabels[i], "Challenge Options"));
    }

    for (let i = 0; i < challenges.length; i++) {
        fadeInChallenge(challenges[i], i);
    }
}