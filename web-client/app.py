from flask import Flask, render_template, request, redirect, url_for, make_response, jsonify

import os
import sys
import uuid
import pymongo
import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import requests
from flask import session

# instantiate the app
app = Flask(__name__)
app.secret_key = os.getenv("SESSION_KEY")

# connect to the database
cxn = pymongo.MongoClient(os.getenv("MONGO_URI"),
                          serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    # The ping command is cheap and does not require auth.
    cxn.admin.command('ping')
    db = cxn[os.getenv("MONGO_DBNAME")]  # store a reference to the database
    # if we get here, the connection worked!
    print(' *', 'Connected to MongoDB!')
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB")
    print('Database connection error:', e)  # debug

# web MongoClient
user_collection = db.user


@app.route('/')
def index():
    """
    Route for the chatroom page :D
    """
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    else:
        return render_template('chatroom.html')


# register page
# capture register date and online date
@app.route('/register', methods=['GET', 'POST'])
def regis():
    """
    Route for the register page
    """
    if request.method == 'POST':
        json_data = request.form
        reg_date = str(datetime.date.today())
        cur = {"username": json_data.get("floatingInput"), "password": json_data.get("floatingPassword"),
               "reg_date": reg_date, "num_chat": 0, "last_online": "None", "log_time": reg_date}
        # check if the username is already in the database
        if user_collection.find_one({'username': json_data.get('floatingInput')}) != None:
            return render_template('register.html', ActExist=True)
        user_collection.insert_one(cur)
        return render_template('login.html', CreAct=True)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        json_data = request.form
        cur = user_collection.find_one(
            {'username': json_data.get('floatingInput')})
        if cur == None:
            return render_template('login.html', NoAct=True)
        else:
            # Update last_online upon login
            if cur['password'] == json_data.get('floatingPassword'):
                log_time = str(datetime.date.today())
                last_online = cur["log_time"]
                username = cur["username"]
                user_collection.update_one({"username": username}, {
                                           "$set": {"last_online": last_online, "log_time": log_time}})
                # save username and user_id in session
                session['username'] = cur['username']
                session['user_id'] = str(cur['_id'])

                return redirect("/")
            else:
                return render_template('login.html', NoAct=True)
    else:
        return render_template('login.html')


# route for chat history
@app.route('/history/')
@app.route('/history/<date_range>')
def history(date_range=None):
    if "username" not in session or "user_id" not in session:
        return redirect("/login")
    uid = session['user_id']
    if date_range is None:
        date_range = 'all'
    if date_range == 'today':
        today = datetime.datetime.now()
        today = datetime.datetime(today.year, today.month, today.day)
        today = datetime.datetime.timestamp(today)
        today = Timestamp(int(today), 0)
        chat_log = db.chat.find({
            '$or': [
                {'from_id': ObjectId(uid)},
                {'to_id': ObjectId(uid)}
            ],
            'timestamp': {'$gte': today}
        }).sort('timestamp', pymongo.ASCENDING).limit(30)
    elif date_range == 'this_week':
        today = datetime.datetime.now()
        today = datetime.datetime(today.year, today.month, today.day)
        last_week = today - datetime.timedelta(days=7)
        last_week = datetime.datetime.timestamp(last_week)
        last_week = Timestamp(int(last_week), 0)
        chat_log = db.chat.find({
            '$or': [
                {'from_id': ObjectId(uid)},
                {'to_id': ObjectId(uid)}
            ],
            'timestamp': {'$gte': last_week}
        }).sort('timestamp', pymongo.ASCENDING).limit(30)
    elif date_range == 'all':
        chat_log = db.chat.find({
            '$or': [
                {'from_id': ObjectId(uid)},
                {'to_id': ObjectId(uid)}
            ]
        }).sort('timestamp', pymongo.ASCENDING).limit(30)
    else:
        return render_template('error.html', error='Invalid date range'), 404
    res = []
    for doc in chat_log:
        doc['timestamp'] = datetime.datetime.fromtimestamp(
            doc['timestamp'].time)
        doc['timestamp'] = doc['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        doc['is_bot'] = doc['to_id'] == ObjectId(uid)
        res.append(doc)
    return render_template('history.html', chat_log=res)


# account profile page
@app.route('/profile')
def profile():
    user_id = session['user_id']
    current_user = user_collection.find_one(({'_id': ObjectId(user_id)}))
    username = current_user["username"]
    signup = current_user["reg_date"]
    last_login = current_user["last_online"]
    chat_history = db.chat.count_documents({'from_id': ObjectId(user_id)})
    return render_template('profile.html', email=username, signup=signup, login=last_login, chat_history=chat_history)


# Edit account page
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id = session['user_id']
    if request.method == 'POST':
        changed_email = request.form["email"]
        changed_password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        doc = {}
        if len(changed_email) == 0 and len(changed_password) == 0 and len(confirm_password) == 0:
            return render_template('edit.html', message="No changes made")
        if len(changed_password) != 0 or len(confirm_password) != 0:
            if changed_password != confirm_password:
                return render_template('edit.html', message="Failed password confirmation")
        if len(changed_email) != 0:
            if not user_collection.find_one({'username': changed_email}) is None:
                return render_template('edit.html', message="Email taken")
            doc["username"] = changed_email
            session['username'] = changed_email
        if len(changed_password) != 0:
            doc["password"] = changed_password
        user_collection.update_one({'_id': ObjectId(user_id)}, {"$set": doc})
        return redirect(url_for("profile"))
    return render_template('edit.html')


# route for chatroom audio transcribe
@app.route('/chatroom/audio', methods=['POST'])
def handle_audio_upload():
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    files = request.files
    file = files.get('fileBlob')

    save_filename = f"{str(uuid.uuid4())}.wav"
    save_filepath = os.path.join("audios", save_filename)
    file.save(save_filepath)

    if os.path.isfile(save_filepath):
        res = requests.post("http://ml-client:5001/transcribe", json={
            "file_name": save_filename
        }, headers={
            "Content-Type": "application/json; charset=utf-8"
        }).json()

        if res["success"] and res["transcript"]["text"] != "":
            db.chat.insert_one({
                "from_id": ObjectId(session["user_id"]),
                "to_id":  ObjectId("639fda7d0de2ac51cade9615"),
                "text": res["transcript"]["text"],
                "timestamp": Timestamp(int(datetime.datetime.now().timestamp()), 1)
            })

        return jsonify(res)
    else:
        return jsonify({
            "success": 0,
            "message": "Error occurred when saving file"
        })


# route for chatroom audio transcribe
@app.route('/chatroom/response', methods=['POST'])
def handle_bot_response():
    if "username" not in session or "user_id" not in session:
        return redirect("/login")

    data = request.json
    print("data:", data)

    prompt = data["prompt"]
    print("prompt:", prompt)

    res = requests.post("http://ml-client:5001/openAI", json={
        "prompt": prompt
    }, headers={
        "Content-Type": "application/json; charset=utf-8"
    }).json()

    db.chat.insert_one({
        "from_id": ObjectId("639fda7d0de2ac51cade9615"),
        "to_id": ObjectId(session["user_id"]),
        "text": res["response"],
        "timestamp": Timestamp(int(datetime.datetime.now().timestamp()), 1)
    })

    return jsonify(res)


# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e), 404  # render the edit template


# run the app
if __name__ == "__main__":
    app.run(debug=True)
