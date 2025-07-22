from flask import Flask, flash, redirect, render_template, request, jsonify, session
# import google.generativeai as genai
from google import genai
import os
from dotenv import load_dotenv 
from flask_session import Session
from functools import wraps
from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp

load_dotenv()
api_key = os.environ.get("GENAI_KEY")

client = genai.Client(api_key=api_key)

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

db = SQL("sqlite:///project.db")

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":

        if not request.form.get("username"):
            return render_template("apology.html")

        elif not request.form.get("password"):
             return render_template("apology.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
             return render_template("apology.html")

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    if username == "" or len(db.execute('SELECT username FROM users WHERE username = ?', username)) > 0:
        return render_template("apology.html")
    if password == "" or password != confirmation:
         return render_template("apology.html")
    db.execute('INSERT INTO users (username, hash) \
            VALUES(?, ?)', username, generate_password_hash(password))
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)
    session["user_id"] = rows[0]["id"]
    session["username"] = rows[0]["username"]
    # Redirect user to home page
    return redirect("/")


@app.route("/ai_data",methods=['GET',"POST"])
def ai_data():
    if request.method == "POST":
        data = request.get_json()
        text = data.get("prompt")
        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=text,
        )
        text = response.candidates[0].content.parts[0].text
        data = {
                "ai_text" : text
            }
        return jsonify(data)
    #     generation_config = {
    #             "temperature": 0.5,
    #             "top_p": 1,
    #             "top_k": 1,
    #             "max_output_tokens": 300,
    #             }

    #     safety_settings = [
    #         {
    #             "category": "HARM_CATEGORY_HARASSMENT",
    #             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #         },
    #         {
    #             "category": "HARM_CATEGORY_HATE_SPEECH",
    #             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #         },
    #         {
    #             "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    #             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #         },
    #         {
    #             "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    #             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    #         }
    #         ]

    #     model = genai.GenerativeModel(model_name="gemini-pro",
    #                                     generation_config=generation_config,
    #                                     safety_settings=safety_settings)

    #     convo = model.start_chat(history=[
    #         {
    #             "role": "user",
    #             "parts": "hi<div><br></div>"
    #         },
    #         {
    #             "role": "model",
    #             "parts": "Hello! How can I help you today?"
    #         }
    #         ])
    #     print("text")
    #     data = request.get_json()
    #     text = data.get("prompt")
    #     print(text)
    #     if text:
    #         # model = genai.Model(name='gemini-pro')
    #         # response = model.generate_content(text)

    #         convo.send_message(text)
    #         response = convo.last.text
    #         print(convo.last.text)
    #         data = {
    #             "ai_text" : response
    #         }
    #         return jsonify(data)
    #     print("there is no text")
    #     print(text)
    # else:
    #     print("text")
    #     data = {
    #         "error": "error"
    #     }









@app.route("/", methods=['GET'])
@login_required
def query_view():
    return render_template('index.html', username =  session.get("username"))


if __name__ == "__main__":
    app.run(debug=True)
