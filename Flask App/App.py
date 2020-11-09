from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

@app.route("/", methods=['GET'])
def installs():
    if request.method == 'GET':
        return render_template("install.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        print(f"Username : {request.form['username']}\nEmail : {request.form['email']}\nPassword : {request.form['password']}")
        return redirect("/main")

if __name__ == "__main__":
    app.run(debug=True)