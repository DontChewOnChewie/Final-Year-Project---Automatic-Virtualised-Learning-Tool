/*
    File used to manage the first upload stage of a lesson.
*/

let banner_input, banner_img;

// Function used to set the banner image to the users chosen image.
const setCurrentlySelectedBanner = (e) => {
    banner_img.src = URL.createObjectURL(e.target.files[0]);
}

window.onload = function () {
    run_globals();
    banner_input = document.querySelector("input[name='thumb']");
    banner_img = document.querySelector("form img");
    banner_input.onchange = (e) => { setCurrentlySelectedBanner(e); }
}