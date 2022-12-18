from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import dotenv_values

import pymongo
import datetime
from bson.objectid import ObjectId
from bson.timestamp import Timestamp
import sys

# instantiate the app
app = Flask(__name__)

# load credentials and configuration options from .env file
# if you do not yet have a file named .env, make one based on the template in env.example
config = dotenv_values(".env")

# turn on debugging if in development mode
if config['FLASK_ENV'] == 'development':
    # turn on debugging, if in development
    app.debug = True # debug mnode


# connect to the database
cxn = pymongo.MongoClient(config['MONGO_URI'], serverSelectionTimeoutMS=5000)
try:
    # verify the connection works by pinging the database
    cxn.admin.command('ping') # The ping command is cheap and does not require auth.
    db = cxn[config['MONGO_DBNAME']] # store a reference to the database
    print(' *', 'Connected to MongoDB!') # if we get here, the connection worked!
except Exception as e:
    # the ping command failed, so the connection is not available.
    print(' *', "Failed to connect to MongoDB at", config['MONGO_URI'])
    print('Database connection error:', e) # debug

# set up the routes
# add statistics display to home page
# route for the home page

# web MongoClient
user_collection = db.user
log_in = False

# login page
@app.route('/')
def login():
    """
    Route for the login page
    """
    global log_in
    log_in = False
    return render_template('login.html')



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
        if user_collection.find_one({'username':json_data.get('floatingInput')}) != None:
            return render_template('register.html', ActExist = True)
        user_collection.insert_one(cur)
        return render_template('login.html', CreAct = True)
    return render_template('register.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
    global log_in
    if request.method == 'POST':
        json_data = request.form
        cur = user_collection.find_one({'username':json_data.get('floatingInput')})
        if cur==None:
            return render_template('login.html', NoAct=True)
        else:
            # Update last_online upon login
            if cur['password'] == json_data.get('floatingPassword'):
                log_time = str(datetime.date.today())
                last_online = cur["log_time"]
                username = cur["username"]
                user_collection.update_one({"username": username}, {"$set": {"last_online": last_online, "log_time": log_time}})
                log_in = True
            else:
                return render_template('login.html', NoAct=True)
    else:
        if log_in == False:
            return render_template('login.html')
    """
    Route for the home page
    """
    jobs = db.jobs.find()
    str_submitted = "Jobs in database: " + str(db.jobs.count_documents({})) + "\n"
    num_succeed = db.jobs.count_documents({"status": "COMPLETED"})
    str_succeed = "Jobs succeeded: " + str(num_succeed) + "\n"
    num_failed = db.jobs.count_documents({"status": "FAILED"})
    str_failed = "Jobs failed: " + str(num_failed) + "\n"
    str_processing = "Jobs processing: " + str(db.jobs.count_documents({"status": "IN_PROCESS"})) + "\n"
    if num_failed + num_succeed != 0:
        success_rate = round((num_succeed/(num_succeed+num_failed))*100)
    else:
        success_rate = 0
    str_success_rate = "Success rate: " + str(success_rate) + "%\n"
    avg_completion = "Average completion time of jobs: INVALID"
    avg_wait = "Average wait time of jobs: INVALID"
    if num_succeed != 0:
        success_doc = db.jobs.find({"status": "COMPLETED"})
        total_completion = datetime.timedelta()
        total_wait = datetime.timedelta()
        for each in success_doc:
            completion = each["completion_time"] - each["start_time"]
            wait = each["start_time"] - each["creation_time"]
            total_completion += completion
            total_wait += wait
        avg_completion = "Average completion time of jobs: " + str((total_completion / num_succeed).total_seconds()) + "s"
        avg_wait = "Average wait time of jobs: " + str((total_wait / num_succeed).total_seconds()) + "s"
    return render_template('index.html', jobs=jobs, submitted=str_submitted,
                           num_succeed=str_succeed, failed=str_failed, processing=str_processing,
                           success_rate=str_success_rate, avg_completion=avg_completion, avg_wait=avg_wait)
    # render the home template

# route for job page
# add statistics display to job page
@app.route('/job/<job_id>')
def job(job_id):
    """
    Route for the job page
    """
    job = db.jobs.find_one({'_id': ObjectId(job_id)})
    if job["status"] == "COMPLETED":
        total_time = 0
        total_confidence = 0
        count = 0
        for i in range(len(job["transcript_items"])):
            if job["transcript_items"][i]["type"] == "pronunciation":
                time_added = float(job["transcript_items"][i]["end_time"])\
                             - float(job["transcript_items"][i]["start_time"])
                confidence_added = float(job["transcript_items"][i]["alternatives"][0]["confidence"])
                total_time += time_added
                total_confidence += confidence_added
                count += 1
        if count != 0:
            avg_confidence = str(round((total_confidence/count)*100, 2)) + "%"
            avg_time = str(round(total_time/count, 3)) + "s"
        else:
            avg_confidence = "INVALID"
            avg_time = "INVALID"
    else:
        avg_confidence = "INVALID"
        avg_time = "INVALID"
    return render_template('job.html', job=job, avg_time=avg_time, avg_confidence=avg_confidence)


# route for chat history
@app.route('/history/')
@app.route('/history/<date_range>')
def history(date_range=None):
    uid = '639e28607c6eba5ef2939c4b' # ???
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
        doc['timestamp'] = datetime.datetime.fromtimestamp(doc['timestamp'].time)
        doc['timestamp'] = doc['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        doc['is_bot'] = doc['to_id'] == ObjectId(uid)
        res.append(doc)
    return render_template('history.html', chat_log=res)


# account profile page
# waiting for flask session to be implemented
@app.route('/profile')
def profile():
    user_id = "639ed925fdbaf2074da8911b" # an existing id for testing
    current_user = user_collection.find_one(({'_id': ObjectId(user_id)}))
    username = current_user["username"]
    signup = current_user["reg_date"]
    last_login = current_user["last_online"]
    chat_history = current_user["num_chat"]
    return render_template('profile.html', email=username, signup=signup, login=last_login, chat_history=chat_history)


# Edit account page
# Waiting for flask session to be implemented
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    user_id = "639ed925fdbaf2074da8911b" # an existing id for testing
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
        if len(changed_password) != 0:
            doc["password"] = changed_password
        user_collection.update_one({'_id': ObjectId(user_id)}, {"$set": doc})
        return redirect(url_for("profile"))
    return render_template('edit.html')


# route to handle any errors
@app.errorhandler(Exception)
def handle_error(e):
    """
    Output any errors - good for debugging.
    """
    return render_template('error.html', error=e), 404 # render the edit template

  
# run the app
if __name__ == "__main__":
    app.run(debug = True)