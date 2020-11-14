from flask import Flask, render_template, request, make_response, redirect, url_for
from Challenge import Challenege
from UserDao import UserDao
from User import User
from EncryptionService import EncryptionService
from SessionDao import SessionDao

app = Flask(__name__)

@app.route("/", methods=['GET'])
def installs():
    if request.method == 'GET':
        return render_template("install.html",
                                show_options = False)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        error = request.cookies.get("error")

        return render_template("login.html",
                                show_options = False,
                                error = error)
    elif request.method == "POST":
        credentials = [request.form['username'], request.form['email'], request.form['password']]
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 

        try:
            enable_auto_login = request.form['stay_signed_in']
        except KeyError:
            enable_auto_login = None
            pass # Catch weird checkbox glitch.

        if credentials:
            udao = UserDao()
            result = udao.login(credentials, ip, auto_login) if udao.check_account_exists(credentials) else udao.signup(credentials, ip, auto_login) 

        if isinstance(result[0], User):
            resp = make_response(redirect("/main")) if not enable_auto_login else make_response(redirect("/autologinsetup"))
            resp.set_cookie("sk", result[1])
            resp.set_cookie("user", result[0].username)
        else:
            resp = make_response(redirect("/login"))
            resp.set_cookie("error", result)

        return resp

@app.route("/autologinsetup", methods=['GET'])
def auto_login_setup():
    if request.method == "GET":
        user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 

        es = EncryptionService()
        encryption_info = es.encrypt(user + ":" + sk)
        udao = UserDao()
        user_id = udao.get_user_id_from_name_and_session_key(user, sk)
        sdao = SessionDao()
        sdao.store_autologin_details(user_id, ip, encryption_info[0], encryption_info[1], encryption_info[2])

        resp = make_response(render_template("autologinsetup.html"))
        resp.set_cookie("data", encryption_info[2])

        return resp

@app.route("/autologin", methods=['GET'])
def auto_login():
    auto_creds = request.args.get("data")
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 

    sdao = SessionDao()
    session = sdao.get_auto_login_key(auto_creds, ip)

    if isinstance(session, str):
        resp = make_response(redirect("/login"))
        resp.set_cookie("error", session)
        return resp

    es = EncryptionService()
    decrypted_creds = es.decrypt(session[6], session[7], session[8]).split(":")

    udao = UserDao()
    udao.auto_login(decrypted_creds[0], decrypted_creds[1])

    resp = make_response(redirect("/main"))
    resp.set_cookie("user", decrypted_creds[0])
    resp.set_cookie("sk", decrypted_creds[1])

    return resp

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

@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        print(user)
        return render_template("account.html")


if __name__ == "__main__":
    app.run(debug=True)