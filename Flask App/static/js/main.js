let playBtns, delPcBtns, delServerBtns, eventHoverLabels;

const setHoverEventLabel = (target, text) => {
    target.innerText = text;
}

window.onload = function () {
    run_globals();
    get_user_downloaded_challenges(document.getElementById("my-list"));

    delServerBtns = document.getElementsByClassName("delete-server-button");
    delPcBtns = document.getElementsByClassName("delete-pc-button");
    playBtns = document.getElementsByClassName("play-button");
    eventHoverLabels = document.getElementsByClassName("hover-event");

    for (let i = 0; i < delServerBtns.length; i++) {
        delServerBtns[i].addEventListener("mouseover", () => setHoverEventLabel(eventHoverLabels[i], "Remove Challenge from Server"));
        delServerBtns[i].addEventListener("mouseout", () => setHoverEventLabel(eventHoverLabels[i], "Challenge Options"));
        delPcBtns[i].addEventListener("mouseover", () => setHoverEventLabel(eventHoverLabels[i], "Remove Challenge from PC"));
        delPcBtns[i].addEventListener("mouseout", () => setHoverEventLabel(eventHoverLabels[i], "Challenge Options"));
        playBtns[i].addEventListener("mouseover", () => setHoverEventLabel(eventHoverLabels[i], "Go to Challenge"));
        playBtns[i].addEventListener("mouseout", () => setHoverEventLabel(eventHoverLabels[i], "Challenge Options"));
    }
}