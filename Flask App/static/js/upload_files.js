 let dropzones, btn_submit;
 let files = [null, null];
 let types = [null, null];
 let footer_a;

const checkUploadType = (type, filename) => {
    if (type == null || filename == null) return false;

    switch (type) {
        case "Docker":
            if (!filename.endsWith(".zip")) return false;
            break;
        case "VirtualBox":
            if (!filename.endsWith(".vdi") && !filename.endsWith(".vmdk") && !filename.endsWith(".iso")) return false;
            break;
        default:
            return false;
    }

    return true;
}

const addUploadItem = (dropzone, data) => {
    let selected_tech = dropzone.getAttribute("data-upload-type");

    if (checkUploadType(selected_tech, data.name)) {
        let index = Array.prototype.indexOf.call(dropzones, dropzone);
        files[index] = data;
        types[index] = selected_tech;
        dropzone.className = "dropzone populated";
    } else {
        dropzone.style.backgroundColor = "#d14848";
        setTimeout(() => { dropzone.style.backgroundColor=""; }, 500);
    }
}

const upload = () => {
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

 window.onload = () => {
     //run_globals();
     dropzones = document.getElementsByClassName("dropzone");
     btn_submit = document.querySelector(".standard-button");

     for (var i = 0; i < dropzones.length; i++) {
        dropzones[i].ondrop = (e) => {
            e.preventDefault();
            addUploadItem(e.target, e.dataTransfer.files[0]);
        }

         dropzones[i].ondragover = () => { return false; }

         dropzones[i].ondragleave = () => { return false; }  
     }

     btn_submit.addEventListener("click", function () { upload(); });
 }