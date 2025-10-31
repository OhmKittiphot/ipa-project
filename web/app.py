from flask import Flask, render_template, request, redirect
import mysql.connector
import os
import time

app = Flask(__name__)


# Connect DB
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv(
        "DB_NAME",
    ),
)
cursor = db.cursor(dictionary=True)


# Main
@app.route("/", methods=["GET"])
def index():
    cursor.execute("SELECT * FROM routers")
    routers = cursor.fetchall()
    return render_template("index.html", routers=routers)


# Router Details
@app.route("/router/<ip>", methods=["GET"])
def get_router(ip):
    db.reconnect()
    cursor = db.cursor(dictionary=True)

    query = """
        SELECT t1.*
        FROM interface_status t1
        INNER JOIN (
            SELECT interface_name, MAX(last_checked) AS latest
            FROM interface_status
            WHERE router_ip = %s
            GROUP BY interface_name
        ) t2 ON t1.interface_name = t2.interface_name AND t1.last_checked = t2.latest
        WHERE t1.router_ip = %s
        ORDER BY t1.interface_name;
    """

    cursor.execute(query, (ip, ip))
    router_details = cursor.fetchall()
    cursor.close()

    return render_template(
        "router_detail.html",
        router_ip=ip,
        router_details=router_details,
    )


# Monitor
@app.route("/toggle_interface_monitor/<int:id>", methods=["POST"])
def toggle_interface_monitor(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT is_monitored FROM interface_status WHERE id = %s", (id,))
    result = cursor.fetchone()

    if result:
        new_value = not result["is_monitored"]
        cursor.execute(
            "UPDATE interface_status SET is_monitored = %s WHERE id = %s",
            (new_value, id),
        )
        db.commit()

    cursor.close()
    referer = request.headers.get("Referer", "/")
    return redirect(referer)


# Add Router
@app.route("/add", methods=["POST"])
def add_router():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        cursor.execute(
            """
            INSERT INTO routers (ip, username, password)
            VALUES (%s, %s, %s)
        """,
            (ip, username, password),
        )
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
