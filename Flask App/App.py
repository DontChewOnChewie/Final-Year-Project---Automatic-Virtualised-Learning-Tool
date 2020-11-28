from flask import Flask, render_template, request, make_response, redirect, url_for
from Challenge import Challenge
from UserDao import UserDao
from User import User
from EncryptionService import EncryptionService
from SessionDao import SessionDao
from UploadHandler import UploadHandler
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
        credentials = [request.form['username'].lower(), request.form['email'], request.form['password']]
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
            if not enable_auto_login:
                resp = make_response(render_template("loginsetup.html", 
                                                    redirect = "/main"))
            else:
                resp = make_response(redirect("/autologinsetup"))

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
    user = udao.auto_login(decrypted_creds[0], decrypted_creds[1])
    udao.close()

    if not user:
        resp = make_response(redirect("/login"))
        return resp

    resp = make_response(render_template("loginsetup.html",
                                            redirect = "/main"))
    resp.set_cookie("user", decrypted_creds[0])
    resp.set_cookie("sk", decrypted_creds[1])

    return resp

@app.route("/main", methods=['GET'])
def main():
    if request.method == "GET":
        get_args = request.args.get("list")
        print(get_args)
        cdao = ChallengeDAO()
        new_challenges = cdao.get_recent_challenges()

        my_challenges = None
        challenges = ""
        if get_args:
            get_args = get_args.split(",")
            for c in get_args:
                challenges += c + "|"
            my_challenges = cdao.get_downloaded_challenges(challenges)

        cdao.close()

        resp = make_response(render_template("main.html",
                                            show_options = True,
                                            new_challenges = new_challenges,
                                            my_challenges = my_challenges))
        resp.set_cookie("challenges", challenges[:-1])
        return resp

@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        logged_user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        challenges = request.cookies.get("challenges")
        udao = UserDao()
        users_page = udao.get_user_from_username(user)

        users_challenges = []
        if users_page:
            cdao = ChallengeDAO(conn=udao.conn)
            users_challenges = cdao.get_users_uploaded_challenges(users_page.id)

        valid_key = False
        my_challenges = None
        if logged_user == user:
            valid_key = udao.check_session_key(logged_user, sk)
            if challenges and valid_key:
                my_challenges = cdao.get_downloaded_challenges(challenges)
            
        udao.close()
        return render_template("account.html",
                                show_options = True,
                                page_owner = users_page,
                                owns_page = valid_key,
                                users_challenges = users_challenges,
                                my_challenges = my_challenges)

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

            if (isinstance(challenge, str)):
                resp = make_response(redirect("/upload"))
                resp.set_cookie("error", challenge)
                return resp
                
            challenge_id = cdao.get_challenge_id_from_user_and_name(challenge.user_id, challenge.name)
            udao.close()

            if challenge:
                uh = UploadHandler()
                result = uh.save_challenege_banner(challenge_id, thumb)
                resp = make_response(redirect(f"/upload/{challenge_id}/files"))
                if isinstance(result, str):
                    resp.set_cookie("error", result)
                return resp

        #print(f"Name : {name}\nDescription : {desc}\nDifficulty : {difficulty}\nDocker : {docker}\nVB : {vb}")
        return redirect("/main")

@app.route("/upload/<id>/files", methods=['GET', 'POST'])
def upload_files(id):
    if request.method == "GET":
        user = request.cookies.get("user")
        sk = request.cookies.get("sk")

        udao = UserDao()
        valid_key = udao.check_session_key(user, sk)
        user = udao.get_user_from_username(user)
        cdao = ChallengeDAO(conn=udao.conn)
        challenge = cdao.get_challenge_by_id(id)

        allowed_edit = True
        if challenge:
            if challenge.user_id != user.id or not valid_key:
                allowed_edit = False
        else:
            redirect("/main") # Redirect to  custom 404 eventually.

        return render_template("upload_files.html",
                                show_options = True,
                                allowed_edit = allowed_edit, 
                                challenge = challenge)
    elif request.method == "POST":
        user = request.cookies.get("user")
        sk = request.cookies.get("sk")

        udao = UserDao()
        valid_key = udao.check_session_key(user, sk)
        user = udao.get_user_from_username(user)
        cdao = ChallengeDAO(conn=udao.conn)
        challenge = cdao.get_challenge_by_id(id)

        if challenge:
            if challenge.user_id != user.id or not valid_key:
                return "0"
        else:
            return "0"

        files_uploads = {}
        for key in request.form.keys():
            files_uploads[key] = [request.form[key], request.files[key]]
        
        print(files_uploads)

        uh = UploadHandler()
        uh.save_challenge_files(files_uploads, challenge.id)
        
        return "1"

@app.route("/challenge/<id>", methods=['GET'])
def challenge(id):
    if request.method == 'GET':
        error = request.cookies.get("error")
        author = None
        banner_path = None
        download_path = None
        cdao = ChallengeDAO()
        challenge = cdao.get_challenge_by_id(id)

        if challenge:
            author = cdao.get_author_of_challenge(id)
            cdao.close()
            uh = UploadHandler()
            banner_path = uh.get_upload_banner_path(str(challenge.id))

            if os.path.isfile(f"static/Challenges/{id}/build.zip"):
                print("Found")
                download_path = f"/static/Challenges/{id}/build.zip"

        return render_template("challenge.html",
                                show_options = True,
                                challenge = challenge,
                                author = author,
                                banner_path = banner_path,
                                download_path = download_path,
                                error = error)

if __name__ == "__main__":
    if not os.path.isdir("static/Challenges"):
        os.mkdir("static/Challenges")
        
    app.run(debug=True)