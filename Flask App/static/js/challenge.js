let download_btn;

window.onload = function () {
    run_globals();

    download_btn = document.querySelector("footer a" );
    // Function in config_manager.js
    // Disables download if user already has it on the system, even on another account.
    download_btn.addEventListener("click", function (e) {
        if (!add_challenge_to_user()) {
            e.preventDefault();
        }
    });

}