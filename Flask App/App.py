from flask import Flask, render_template, request, make_response, redirect
from Challenge import Challenege

app = Flask(__name__)

@app.route("/", methods=['GET'])
def installs():
    if request.method == 'GET':
        return render_template("install.html",
                                show_options = False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html",
                                show_options = False)
    elif request.method == "POST":
        print(f"Username : {request.form['username']}\nEmail : {request.form['email']}\nPassword : {request.form['password']}")
        return redirect("/main", 
                        show_options = True)

@app.route("/main", methods=['GET'])
def main():
    if request.method == "GET":
        return render_template("main.html",
                                show_options = True,
                                new_challenges = [Challenege("Challenege 1", None, Challenege.Difficulty.BEGGINER, None, [Challenege.Technology.VB]),
                                                  Challenege("Challenege 2", None, Challenege.Difficulty.INTERMEDIATE, None, [Challenege.Technology.DOCKER]),
                                                  Challenege("Challenege 3", None, Challenege.Difficulty.ADVANCED, None, [Challenege.Technology.DOCKER, Challenege.Technology.VB]),
                                                  Challenege("Challenege 4", None, Challenege.Difficulty.INTERMEDIATE, None, [Challenege.Technology.DOCKER]),
                                                ], 
                                users_list = [Challenege("Challenege 1", None, Challenege.Difficulty.BEGGINER, None, [Challenege.Technology.VB]),
                                                  Challenege("Challenege 2", None, Challenege.Difficulty.INTERMEDIATE, None, [Challenege.Technology.DOCKER]),
                                                  Challenege("Challenege 3", None, Challenege.Difficulty.ADVANCED, None, [Challenege.Technology.DOCKER, Challenege.Technology.VB]),
                                                  Challenege("Challenege 4", None, Challenege.Difficulty.INTERMEDIATE, None, [Challenege.Technology.DOCKER]),
                                                ])

if __name__ == "__main__":
    app.run(debug=True)