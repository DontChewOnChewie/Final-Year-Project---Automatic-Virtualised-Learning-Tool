let scroll_btns;

function scroll_carousel(carousel_btn) {
    let p = carousel_btn.parentElement;
    let pp = carousel_btn.parentElement.parentElement;
    let scrolled = pp.getAttribute("data-scrolled");
    
    if (scrolled == "0") {
        p.style.left = "98%";
        pp.style.left = "-100%";
        pp.setAttribute("data-scrolled", "1");    
        carousel_btn.style.transform = "rotate(180deg)";
    } else {
        p.style.left = "48%";
        pp.style.left = "0%";
        pp.setAttribute("data-scrolled", "0");
        carousel_btn.style.transform = "rotate(0deg)";
    }

}

window.onload = function () {
    run_globals();
    get_user_downloaded_challenges(document.getElementById("my-list"));
    
    scroll_btns = document.querySelectorAll(".scroller img");

    for (var i = 0; i < scroll_btns.length; i++) {
        scroll_btns[i].addEventListener("click", function () {
                scroll_carousel(this);
        });
    }
}