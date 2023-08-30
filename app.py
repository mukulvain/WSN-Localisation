from flask import Flask, request
import json
app = Flask(__name__)

@app.route('/wifi_environments', methods=["GET", 'POST'])
def collect_data():
    if request.method == "GET":
        return json.dumps({
            "STATUS": "UP AND RUNNING"
        })
    json_data = request.get_json()
    print(json_data)
    return json.dumps({"status": "OK", "message": "Successful"})
