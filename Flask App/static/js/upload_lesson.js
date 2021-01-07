let builder, builder_output, add_task_btn;
let upload_btn;
let type_codes = {"Info":"0", "Input":"1", "Checkbox":"2"};

function upload_lesson() {
    upload_btn.innerText = "Uploading...";
    let json = JSON.stringify(get_current_json_output());
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

function update_builder_output() {
    let build = get_current_json_output();
    builder_output.innerHTML = "";
    
    let challenge_title = document.createElement("h2");
    challenge_title.innerText = build.name;
    builder_output.appendChild(challenge_title);

    build.objectives.forEach(task => {
        let task_wrapper = document.createElement("div");
        task_wrapper.className = "task-div";

        let task_title = document.createElement("h3");
        task_title.innerText = task.title;
        let task_description = document.createElement("p");
        task_description.innerText = task.description;
        let task_complete_btn = document.createElement("button");
        task_complete_btn.innerText = "Complete";
        task_complete_btn.type = "button";
        
        task_wrapper.appendChild(task_title);
        task_wrapper.appendChild(task_description);
        task_wrapper.appendChild(task_complete_btn);

        // Input
        if (task.type == "1") {
            let inp_answer = document.createElement("input");
            inp_answer.placeholder = "Answer...";
            task_wrapper.insertBefore(inp_answer, task_complete_btn);
        }

        // Checkbox
        if (task.type == "2") {
            let checkbox_wrapper = document.createElement("div");
            let checkbox_lbl = document.createElement("label");
            checkbox_lbl.innerText = "Have you completed the above?";
            let checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox_wrapper.appendChild(checkbox);
            checkbox_wrapper.appendChild(checkbox_lbl);
            task_wrapper.insertBefore(checkbox_wrapper, task_complete_btn);
        }

        builder_output.appendChild(task_wrapper);
    });
}

function get_current_json_output() {
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

function remove_task_input(obj) {
    let remove_div = obj.parentElement.parentElement;
    builder.removeChild(remove_div);
}

function type_changed(obj) {
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

function add_new_task_inputs() {
    let task_div = document.createElement("div");
    task_div.className = "task-div";

    let header_div = document.createElement("div");
    let title_inp = document.createElement("input");
    title_inp.placeholder = "Task Title...";
    title_inp.className = "inp_title";
    let remove_btn = document.createElement("img");
    remove_btn.src = "/static/images/delete.svg";
    remove_btn.addEventListener("click", function () { remove_task_input(this); });
    header_div.appendChild(title_inp);
    header_div.appendChild(remove_btn);

    let desc_inp = document.createElement("textarea");
    desc_inp.placeholder = "Task Description...";
    desc_inp.className = "inp_desc";

    let task_type_inp  = document.createElement("select");
    task_type_inp.onchange = function () { type_changed(this); }
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
    //run_globals();
    builder = document.querySelector(".builder");
    builder_output = document.querySelector(".lesson-obj");
    add_task_btn = document.getElementById("add-task-btn");
    add_task_btn.addEventListener("click", function () { add_new_task_inputs(); });
    upload_btn = document.getElementById("upload-btn");
    upload_btn.addEventListener("click", function () { upload_lesson(); });

    // Used to update output of builder.
    setInterval(function() { update_builder_output(); }, 5000);
}