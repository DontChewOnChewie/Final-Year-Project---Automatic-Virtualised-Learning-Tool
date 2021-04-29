from flask import Flask, render_template, request, make_response, redirect, url_for
from Challenge import Challenge
from UserDao import UserDao
from User import User
from EncryptionService import EncryptionService
from SessionDao import SessionDao
from UploadHandler import UploadHandler
from ChallengeDAO import ChallengeDAO
import os
import json

app = Flask(__name__)

@app.route("/", methods=['GET'])
def installs():
    if request.method == 'GET':
        return render_template("install.html",
                                show_options = False)

@app.route("/install/manual", methods=['GET'])
def manual_install():
    if request.method == 'GET':
        return render_template("manual_install.html",
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
        
        print(result)
            
        if isinstance(result[0], User):
            resp = make_response(redirect("/main"))
            if enable_auto_login:
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
        error_cookie = request.cookies.get("error")

        cdao = ChallengeDAO()
        new_challenges = cdao.get_recent_challenges()
        cdao.close()

        resp = make_response(render_template("main.html",
                                show_options = True,
                                new_challenges = new_challenges))
        if error_cookie:
            resp.delete_cookie("error")
        return resp

@app.route("/account/<user>", methods=['GET'])
def account(user):
    if request.method == 'GET':
        logged_user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        error = request.cookies.get("error")
        udao = UserDao()
        valid_key = udao.check_session_key(logged_user, sk)
        users_page = udao.get_user_from_username(user)

        users_challenges = []
        if users_page:
            cdao = ChallengeDAO(conn=udao.conn)
            users_challenges = cdao.get_users_uploaded_challenges(users_page.id)
            
        udao.close()

        resp = make_response(render_template("account.html",
                                show_options = True,
                                page_owner = users_page,
                                owns_page = valid_key,
                                users_challenges = users_challenges))
        if error:
            resp.delete_cookie("error")
        return resp

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
                resp = make_response(redirect("/upload/{id}/files".format(id = challenge_id)))
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
        udao.close()

        if challenge:
            if challenge.user_id != user.id or not valid_key:
                return "0"
        else:
            return "0"

        files_uploads = {}
        for key in request.form.keys():
            files_uploads[key] = [request.form[key], request.files[key]]
        

        uh = UploadHandler()
        uh.save_challenge_files(files_uploads, challenge.id)
        
        return "Y"

@app.route("/upload/<id>/lesson", methods=['GET', 'POST'])
def upload_lesson(id):
    if request.method == "GET":
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

        if valid_key:
            cdao = ChallengeDAO(conn=udao.conn)
            challenge = cdao.get_challenge_by_id(id)
            udao.close()
            return render_template("upload_lesson.html",
                                    show_options = True,
                                    challenge = challenge)
        
        return "N"
    elif request.method == "POST":
        user = request.cookies.get("user")
        sk = request.cookies.get("sk")
        json = request.form['json']

        udao = UserDao()
        valid_key = udao.check_session_key(user, sk)
        user = udao.get_user_from_username(user)
        cdao = ChallengeDAO(conn=udao.conn)
        challenge = cdao.get_challenge_by_id(id)
        udao.close()

        if challenge:
            if challenge.user_id != user.id or not valid_key:
                return "0"
            
            uh = UploadHandler()
            result = uh.save_lesson_file(json, id)
            return "Y"

        return "0"

@app.route("/challenge/<id>", methods=['GET'])
def challenge(id):
    if request.method == 'GET':
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
            banner_path = banner_path if banner_path != None else "/static/images/placeholder.jpg"
            print(banner_path)

            if os.path.isfile("static/Challenges/{id}/build.zip".format(id = id)):
                download_path = "/static/Challenges/{id}/build.zip".format(id = id)

        return render_template("challenge.html",
                                show_options = True,
                                challenge = challenge,
                                author = author,
                                banner_path = banner_path,
                                download_path = download_path)

@app.route("/challenge/<id>/delete", methods=['DELETE'])
def delete_challenge(id):
    if request.method == "DELETE":
        user = request.cookies.get("user")
        sk = request.cookies.get("sk")

        udao = UserDao()
        valid_key = udao.check_session_key(user, sk)
        if valid_key:
            user_id = udao.get_user_id_from_name_and_session_key(user, sk)
            cdao = ChallengeDAO(conn=udao.conn)
            owns_challenge = cdao.check_user_owns_challenge(user_id, id)
            if owns_challenge:
                cdao.delete_challenge(id)
                uh = UploadHandler()
                uh.remove_challenge(id)
                cdao.close()
                udao.close()
                return "Y"

        cdao.close()
        udao.close()
        return "Error"


@app.route("/challenge/getuserchallengedata", methods=["GET"])
def get_user_challenge_data():
    if request.method == "GET":
        challenge_ids = request.args.get("obj").split(",")
        challenge_data = {}
        cdoa = ChallengeDAO()
        for i in range(len(challenge_ids)):
            challenge = cdoa.get_challenge_by_id(challenge_ids[i])
            if challenge:
                challenge_data[str(i)] = json.dumps(challenge.__dict__)
        print(challenge_data)
        return challenge_data


@app.route("/settings", methods=["GET"])
def settings():
    if request.method == "GET":
        return render_template("settings.html",
                                show_options = True)

@app.route("/testpage", methods=["GET"])
def testPage():
    if request.method == "GET":
        return render_template("upload_files.html",
                                show_options = True,
                                allowed_edit = True)

if __name__ == "__main__":
    if not os.path.isdir("static/Challenges"):
        os.mkdir("static/Challenges")
        
    app.run(debug=True, host="0.0.0.0")