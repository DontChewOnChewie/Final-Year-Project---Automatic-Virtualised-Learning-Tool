 let dropzones, btn_submit;
 let files = [null, null];
 let types = [null, null];
 let footer_a;

const showUploadingDiv = () => {
    const remove = document.getElementsByClassName("file-upload-wrapper");
    const length = remove.length;
    for (let i = 0; i < length; i++) {
        remove[i].style.opacity = "0";
        setTimeout(() => {
            remove[0].remove();
        }, 1000);
    }

    setTimeout(() => {
        const wrapper = document.createElement("div");
        wrapper.className = "file-upload-wrapper";
        wrapper.style.opacity = "0";

        const zone = document.createElement("div");
        zone.className = "dropzone empty";

        const title = document.createElement("span");
        title.innerText = "Uploading...";

        const img = document.createElement("img");
        img.src = "/static/images/upload_orange.svg";

        const topLoadingBar = document.createElement("div");
        topLoadingBar.className = "loading-bar";
        topLoadingBar.style.zIndex = "-1";
        topLoadingBar.style.backgroundColor = "#0054DC";

        const bottomLoadingBar = document.createElement("div");
        bottomLoadingBar.className = "loading-bar";
        bottomLoadingBar.style.zIndex = "-2";
        bottomLoadingBar.style.backgroundColor = "#6cb85d";

        zone.appendChild(title);
        zone.appendChild(img);
        zone.appendChild(topLoadingBar);
        zone.appendChild(bottomLoadingBar);
        wrapper.appendChild(zone);
        document.querySelector(".upload-wrapper").appendChild(wrapper);
        setTimeout(() => { 
            wrapper.style.opacity = "1";
            topLoadingBar.style.animation = "loading 3s cubic-bezier(0.075, 0.82, 0.165, 1) 2s infinite normal forwards";
            btn_submit.style.display = "none";
        }, 400);
    }, 2500);
}

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

    if (files[0] == null && files[1] == null) {
        for (let i = 0; i < dropzones.length; i++) {
            dropzones[i].style.backgroundColor = "#d14848";
            setTimeout(() => { dropzones[i].style.backgroundColor=""; }, 500);
        }
        return;
    }

    showUploadingDiv();

    let xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200 && this.responseText == "Y") {
            setTimeout(() => {
                // Remove loading bars.
                const loadingDropzone = document.querySelector(".dropzone");
                loadingDropzone.children[2].remove();
                loadingDropzone.children[2].remove();

                // Reset Label
                loadingDropzone.children[0].innerText = "Uploaded";

                // Add next page button
                btn_submit.style.display = "block";
                btn_submit.innerText = "Go to Upload Lesson";
                btn_submit.removeEventListener("click", upload);
                btn_submit.onclick = () => {
                    window.location.href = `${window.location.href.replace("files", "")}lesson`;
                }
            }, 3000);
        }
    };

    xhr.open("post", document.location.href);
    xhr.send(formData);
}

 window.onload = () => {
     run_globals();
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

     btn_submit.addEventListener("click", upload);
 }