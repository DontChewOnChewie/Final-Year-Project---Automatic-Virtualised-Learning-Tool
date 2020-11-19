from flask import Flask, render_template, request, make_response, redirect, url_for
from Challenge import Challenege
from UserDao import UserDao
from User import User
from EncryptionService import EncryptionService
from SessionDao import SessionDao
from FileUploadSanitiser import FileUploadSanitiser
from ChallengeDAO import ChallengeDAO
import os

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
            udao.close()
            
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
        udao.close()

        sdao = SessionDao()
        sdao.store_autologin_details(user_id, ip, encryption_info[0], encryption_info[1], encryption_info[2])
        sdao.close()

        resp = make_response(render_template("autologinsetup.html"))
        resp.set_cookie("data", encryption_info[2])

        return resp

@app.route("/autologin", methods=['GET'])
def auto_login():
    auto_creds = request.args.get("data")
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr) 

    sdao = SessionDao()
    session = sdao.get_auto_login_key(auto_creds, ip)
    sdao.close()

    if isinstance(session, str):
        resp = make_response(redirect("/login"))
        resp.set_cookie("error", session)
        return resp

    es = EncryptionService()
    decrypted_creds = es.decrypt(session[6], session[7], session[8]).split(":")

    udao = UserDao()
    udao.auto_login(decrypted_creds[0], decrypted_creds[1])
    udao.close()

    resp = make_response(redirect("/main"))
    resp.set_cookie("user", decrypted_creds[0])
    resp.set_cookie("sk", decrypted_creds[1])

    return resp

@app.route("/main", methods=['GET'])
def main():
    if request.method == "GET":
        return render_template("main.html",
                                show_options = True,
                                new_challenges = [Challenege(None, "Challenege 1", None, 1, [Challenege.Technology.VB]),
                                                  Challenege(None, "Challenege 2", None, 2, [Challenege.Technology.DOCKER]),
                                                  Challenege(None, "Challenege 3", None, 3, [Challenege.Technology.DOCKER, Challenege.Technology.VB]),
                                                  Challenege(None, "Challenege 4", None, 2, [Challenege.Technology.DOCKER]),
                                                ], 
                                users_list = [Challenege(None, "Challenege 1", None, 1, [Challenege.Technology.VB]),
                                                  Challenege(None, "Challenege 2", None, 2, [Challenege.Technology.DOCKER]),
                                                  Challenege(None, "Challenege 3", None, 3, [Challenege.Technology.DOCKER, Challenege.Technology.VB]),
                                                  Challenege(None, "Challenege 4", None, 2, [Challenege.Technology.DOCKER]),
                                                ])

@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        logged_user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        udao = UserDao()
        users_page = udao.get_user_from_username(user)

        valid_key = False
        if logged_user == user:
            valid_key = udao.check_session_key(logged_user, sk)
            
        udao.close()
        return render_template("account.html",
                                show_options = True,
                                page_owner = user,
                                owns_page = valid_key)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == "GET":
        logged_user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        error = request.cookies.get("error")
        
        udao = UserDao()
        valid_key = udao.check_session_key(logged_user, sk)
        udao.close()

        return render_template("upload.html",
                                show_options = True,
                                signed_in = valid_key,
                                error = error)
    elif request.method == "POST":
        logged_user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        udao = UserDao()

        if udao.check_session_key(logged_user, sk):
            name = request.form['name']
            desc = request.form['desc']
            difficulty = request.form['difficulty']
            thumb = request.files['thumb']

            user = udao.get_user_from_username(logged_user)

            cdao = ChallengeDAO(conn=udao.conn)
            challenge = cdao.add_challenge(int(user.id), name, desc, int(difficulty))
            challenge_id = cdao.get_challenge_from_user_and_name(challenge.user_id, challenge.name)
            udao.close()

            if challenge:
                fup = FileUploadSanitiser()
                result = fup.save_challenege_banner(challenge_id, thumb)
                resp = make_response(redirect(f"/challenge/{challenge_id}"))
                if not result:
                    resp.set_cookie("error", "File could not be uploaded, file type must be png, jpg, jpeg or svg.")
                return resp

        #print(f"Name : {name}\nDescription : {desc}\nDifficulty : {difficulty}\nDocker : {docker}\nVB : {vb}")
        return redirect("/main")

@app.route("/challenge/<id>", methods=['GET'])
def challenge(id):
    if request.method == 'GET':
        error = request.cookies.get("error")
        cdao = ChallengeDAO()
        challenge = cdao.get_challenge_by_id(int(id))
        return render_template("challenge.html",
                                show_options = True,
                                challenge = challenge,
                                error = error)

if __name__ == "__main__":
    if not os.path.isdir("Challenges"):
        os.mkdir("Challenges")
        
    app.run(debug=True)