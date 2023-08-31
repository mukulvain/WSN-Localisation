from flask import Flask, request, send_file, send_from_directory
import json
import datetime
import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)

data = {}
index = 0


@app.route("/wifi_environments", methods=["GET", "POST"])
def collect_data():
    global index, data
    if request.method == "GET":
        return json.dumps({"STATUS": "UP AND RUNNING", "VERSION": "1.0.0"})
    try:
        json_data = request.get_json()
        data[index] = json_data["wifi_networks"]
        index += 1
        return json.dumps({"status": "Accepted", "message": "Data Received"})
    except:
        return json.dumps({"status": "Failed"})


@app.route("/see_data", methods=["GET"])
def see_data():
    return json.dumps(data)


@app.route("/download_data", methods=["GET"])
def save_data():
    global data
    now = int(datetime.datetime.now().timestamp())
    with open(f"database/data_{now}.json", "w") as f:
        json.dump(data, f)
    return send_file(f"database/data_{now}.json", as_attachment=True)


@app.route("/clear_data", methods=["GET"])
def clear_data():
    global data
    password = request.form["password"]
    if password == os.getenv("CLEAR_DATA"):
        data.clear()
        return json.dumps({"status": "Accepted"})
    else:
        return json.dumps({"status": "Failed"})


@app.route("/reset_database", methods=["GET"])
def reset_database():
    password = request.form["password"]
    if password == os.getenv("RESET_DATABASE"):
        current_dir = os.path.join(os.getcwd(), "database")
        files = os.listdir(current_dir)
        for file in files:
            os.remove(os.path.join(current_dir, file))
        return json.dumps({"status": "Accepted"})
    else:
        return json.dumps({"status": "Failed"})
