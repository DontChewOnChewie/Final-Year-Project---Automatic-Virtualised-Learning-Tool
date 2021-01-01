 let dropzones, btn_submit, tech_btns;
 let files = [null, null, null];
 let types = [null, null, null];

 let footer_a;

function toggle_tech(btn) {
    if (btn.getAttribute("data-selected") == "1") return;
    let parent = btn.parentElement;
    for (var i = 0; i < parent.children.length; i++) {
        parent.children[i].className = "";
        parent.children[i].setAttribute("data-selected", "0");
    }

    btn.className = "selected";
    btn.setAttribute("data-selected", "1");
}

function tech_selected(dropzone) {
    let tech_logos = dropzone.parentElement.getElementsByTagName("img");
    for (var i = 0; i < tech_logos.length; i++) {
        if (tech_logos[i].getAttribute("data-selected") == "1") return true;
    }
    return false;
}

function add_upload_item(dropzone, data) {
    if (!tech_selected(dropzone)) return;

    let tech_wrapper = dropzone.parentElement.querySelector(".technoliges-chooser");
    let selected_tech;
    for (var i = 0; i < tech_wrapper.children.length; i++) {
        if (tech_wrapper.children[i].getAttribute("data-selected") == "1") {
            selected_tech = tech_wrapper.children[i].getAttribute("alt").split(" ")[0];
        }
    }

    let index = Array.prototype.indexOf.call(dropzones, dropzone);
    files[index] = data;
    types[index] = selected_tech;
    dropzone.className = "dropzone populated";
}

function upload() {
    let formData = new FormData();
    for (var i = 0; i < files.length; i++) {
        if (files[i] != null) {
            formData.append(`${i}`, files[i]);
            formData.append(`${i}`, types[i]);
        }
    }

    let footer = document.createElement("footer");
    footer.style.width = "100%";
    footer_a = document.createElement("a");
    footer_a.innerText = "Uploading Files...";
    footer.appendChild(footer_a);
    document.querySelector("body").appendChild(footer);

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200 && this.responseText == "Y") {
            let footer_link = document.location.href.substring(0, document.location.href.length - 5);
            footer_a.setAttribute("href", `${footer_link}lesson`);
            footer_a.innerText = "Upload Lesson for Challenge >>";
            footer_a.className = "populated";
        }
    };

    xhr.open("post", document.location.href);
    xhr.send(formData);
}

 window.onload = function () {
     run_globals();
     dropzones = document.querySelectorAll(".dropzone");
     btn_submit = document.querySelector(".standard-button");
     tech_btns = document.querySelectorAll(".technoliges-chooser img");

     for (var i = 0; i < dropzones.length; i++) {
        dropzones[i].ondrop = function (e) {
            e.preventDefault();
            add_upload_item(this, e.dataTransfer.files[0]);
        }

         dropzones[i].ondragover = function () {
            return false;
         }

         dropzones[i].ondragleave = function () {
            return false;
         }  
     }

     btn_submit.addEventListener("click", function () { upload(); });

     for (var i = 0; i < tech_btns.length; i++) {
         tech_btns[i].addEventListener("click", function () { toggle_tech(this); });
     }
 }