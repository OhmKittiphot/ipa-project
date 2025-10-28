from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import time

app = Flask(__name__)


time.sleep(10)

# Connect DB
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME",)
)
cursor = db.cursor(dictionary=True)

# Main
@app.route("/", methods=["GET"])
def index():
    cursor.execute("SELECT * FROM routers")
    routers = cursor.fetchall()
    return render_template("index.html", routers=routers)

# Add Router
@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        cursor.execute("""
            INSERT INTO routers (ip, username, password)
            VALUES (%s, %s, %s)
        """, (ip, username, password))
        db.commit()
    return redirect("/")

# Delete Router
@app.route("/delete/<string:ip>", methods=["POST"])
def delete_router(ip):
    cursor.execute("DELETE FROM routers WHERE ip = %s", (ip,))
    db.commit()
    return redirect("/")

# RUN
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
