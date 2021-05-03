/*
    File used to manage the uploading of user lesson files.
*/

let builder, add_task_btn;
let upload_btn;
let type_codes = {"Info":"0", "Input":"1", "Checkbox":"2"};

// Function used to upload a lesson on button click using XMLHttpRequest.
// Also alert user file has been uploaded on success.
const uploadLesson = () => {
    upload_btn.innerText = "Uploading...";
    let json = JSON.stringify(getCurrentJsonOutput());
    let xhr = new XMLHttpRequest();
    let data = new FormData();
    data.append("json", json);

    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200 && this.responseText == "Y") {
            upload_btn.innerText = "Uploaded! You can edit and reupload still.";
        }
    }

    xhr.open("post", document.location.href);
    xhr.send(data);
}

// Function used to transform the users inputs into a valid json file.
const getCurrentJsonOutput = () => {
    let tasks = builder.querySelectorAll(".task-div");

    // Set up JSON Object;
    let json_obj = {};
    json_obj.name = challenge_name;
    json_obj.objectives = [];

    tasks.forEach(element => {
        let type = element.querySelector("select").value;
        if (type == "0") return;
        
        let objective = {};
        let type_code = type_codes[type];
        let title = element.querySelector(".inp_title").value;
        let desc = element.querySelector(".inp_desc").value;
        objective.type = type_code;
        objective.title = title;
        objective.description = desc;

        if (type == "Input") {
            objective.answers = element.querySelector(".inp_answers").value.split(",");
            objective['case-sensitive'] = element.querySelector("input[type='checkbox']").checked;
        }

        json_obj.objectives.push(objective);
    });

    return json_obj;
}

// Function used to remove an objective the user has outlined.
const removeObjective = (obj) => {
    let remove_div = obj.parentElement.parentElement;
    builder.removeChild(remove_div);
}

// Function used to update the objective input whenever the user changes the type of objective.
const typeChanged = (obj) => {
    let parent = obj.parentElement;
    if (obj.value == "Input") {
        let answers_inp = document.createElement("input");
        answers_inp.placeholder = "Comma Seperated List of Answers...";
        answers_inp.className = "inp_answers";

        let checkbox_wrapper = document.createElement("div");
        let case_sesnsitive_label = document.createElement("label");
        case_sesnsitive_label.innerText = "Case Sensistive?";
        let case_sesnsitive_checkbox = document.createElement("input");
        case_sesnsitive_checkbox.type = "checkbox";
        checkbox_wrapper.appendChild(case_sesnsitive_label);
        checkbox_wrapper.appendChild(case_sesnsitive_checkbox);

        parent.appendChild(answers_inp);
        parent.appendChild(checkbox_wrapper);
    } else {
        try {
            parent.removeChild(parent.getElementsByTagName("div")[1]);
            parent.removeChild(parent.querySelector(".inp_answers"));
        } catch {}
    }
}

// Function used to add a new objective input when the user requests for one.
const addNewObjective = () => {
    let task_div = document.createElement("div");
    task_div.className = "task-div";

    let header_div = document.createElement("div");
    let title_inp = document.createElement("input");
    title_inp.placeholder = "Task Title...";
    title_inp.className = "inp_title";
    let remove_btn = document.createElement("img");
    remove_btn.src = "/static/images/delete.svg";
    remove_btn.addEventListener("click", function () { removeObjective(this); });
    header_div.appendChild(title_inp);
    header_div.appendChild(remove_btn);

    let desc_inp = document.createElement("textarea");
    desc_inp.placeholder = "Task Description...";
    desc_inp.className = "inp_desc";

    let task_type_inp  = document.createElement("select");
    task_type_inp.onchange = function () { typeChanged(this); }
    let option1 = document.createElement("option");
    option1.disable = true;
    option1.hidden = true;
    option1.innerText = "Select a task type...";
    option1.value = "0";
    let option2 = document.createElement("option");
    option2.innerText = "Info";
    let option3 = document.createElement("option");
    option3.innerText = "Input";
    let option4 = document.createElement("option");    
    option4.innerText = "Checkbox";
    task_type_inp.appendChild(option1);
    task_type_inp.appendChild(option2);
    task_type_inp.appendChild(option3);
    task_type_inp.appendChild(option4)

    task_div.appendChild(header_div);
    task_div.appendChild(desc_inp);
    task_div.appendChild(task_type_inp);
    builder.insertBefore(task_div, add_task_btn);
}

window.onload = function () {
    run_globals();
    builder = document.querySelector(".builder");
    add_task_btn = document.getElementById("add-task-btn");
    add_task_btn.addEventListener("click", function () { addNewObjective(); });
    upload_btn = document.getElementById("upload-btn");
    upload_btn.addEventListener("click", function () { uploadLesson(); });
}