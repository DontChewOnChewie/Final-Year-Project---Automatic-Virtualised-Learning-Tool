let banner_input, banner_img;

const setCurrentlySelectedBanner = (e) => {
    banner_img.src = URL.createObjectURL(e.target.files[0]);
}

window.onload = function () {
    run_globals();
    banner_input = document.querySelector("input[name='thumb']");
    banner_img = document.querySelector("form img");
    banner_input.onchange = (e) => { setCurrentlySelectedBanner(e); }
}