💬 Flask Chatbot with Gemini AI
Welcome! This is a simple web chatbot where you can talk to an AI. It's built with Flask (a web tool) and uses Google's Gemini AI. It also has a basic login system to keep your chats private.

✨ What It Does
User Login: Easily create an account and sign in.

AI Chat: Talk to an AI powered by Google's gemini-2.5-flash model.

Safe Keys: Your secret keys are kept secure using a special .env file.

User Data: Saves your account information in a simple database file.

🚀 How It Works
This app uses a few main parts:

Flask (Backend): This is the core of the website, handling pages, logins, and talking to the AI.

User Accounts: It uses a tool called cs50.SQL to store usernames and secure passwords in a file named project.db.

AI Connection: The google-genai library sends your messages to Google's AI model and gets responses back. Your secret AI key is loaded from the .env file.

🛠️ Get Started (Setup and Run)
Follow these steps to get the chatbot running on your computer:

1. What You'll Need
Python 3.9 or newer installed on your computer.

Git (if you're downloading the project files from GitHub).

2. Get Your Google Gemini AI Key
You need a free key to use the AI:

Go to Google AI Studio.

Sign in and create a new API key. Keep this key private!

3. Get the Project Files
First, you'll need to get the project files onto your computer. If you're using Git (recommended):

git clone https://github.com/tousifT5/Chatbot.git
cd your-chatbot-repo

If you're not using Git, you can manually download the project files and then navigate to that folder in your terminal:

cd /path/to/your/project/folder # Example: cd ~/Desktop/user/Projects/Chatbot

4. Install Necessary Tools
In your terminal, run this command to install all the required Python libraries:

pip install Flask python-dotenv Flask-Session cs50 werkzeug google-genai

5. Keep Your Secret Keys Safe
Create a new file called .env in your main project folder (the same place as app.py).

Open .env with a text editor and add these lines:

# .env file
GENAI_KEY="YOUR_GOOGLE_GEMINI_API_KEY_HERE"
FLASK_SECRET_KEY="YOUR_FLASK_SECRET_KEY_HERE"

Important:

Replace "YOUR_GOOGLE_GEMINI_API_KEY_HERE" with the actual key you got from Google AI Studio.

For FLASK_SECRET_KEY, use a very long and random string. You can make one by typing python -c 'import os; print(os.urandom(24).hex())' in your terminal and copying the output.

Never share your .env file or upload it to GitHub! Make sure your .gitignore file lists project.db and .env to keep them private.

6. Set Up the User Database
create a sql database with mentioned schema below
you will find schema.sql it contains schema of database
or you can copy below schema for user database.

CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL);

7. Run the Chatbot!
Now you can start the application. In your terminal, type:

python app.py

Open your web browser and go to http://127.0.0.1:5000/.

📂 Project Files
app.py: The main code for the chatbot and website.

static/project.css: Controls how the website looks.

templates/: All the website pages (apology.html, index.html, register.html, login.html, layout.html).

.gitignore: Tells Git which files to ignore (like your secret keys and database).

project.db: make sure it exist before running app.py

requirements.txt: Lists all the Python libraries this app needs.

⚠️ Important Notes
Key Safety: Always use the .env file for your GENAI_KEY and FLASK_SECRET_KEY. Never share these!
