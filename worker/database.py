import os
from datetime import datetime, timedelta, timezone

import mysql.connector
import requests

THAI_TZ = timezone(timedelta(hours=7))


def save_interface_status(router_ip, interfaces):
    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    conn = mysql.connector.connect(
        host=db_host, user=db_user, password=db_password, database=db_name
    )
    cursor = conn.cursor(dictionary=True)

    for iface in interfaces:
        interface_name = iface.get("interface")
        ip_address = iface.get("ip_address")
        status = iface.get("status")
        proto = iface.get("proto")

        # CHECK DB
        cursor.execute(
            """
            SELECT is_monitored FROM interface_status
            WHERE router_ip = %s AND interface_name = %s
            LIMIT 1
        """,
            (router_ip, interface_name),
        )
        res = cursor.fetchone()
        is_monitored = res["is_monitored"] if res else True

        # UPDATE
        cursor.execute(
            """
            INSERT INTO interface_status
                (router_ip, interface_name, ip_address, status, proto, last_checked)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                ip_address = VALUES(ip_address),
                status = VALUES(status),
                proto = VALUES(proto),
                last_checked = VALUES(last_checked);
        """,
            (
                router_ip,
                interface_name,
                ip_address,
                status,
                proto,
                datetime.now(THAI_TZ),
            ),
        )

        # call notify_discord
        if is_monitored and (status.lower() != "up" or proto.lower() != "up"):
            notify_discord(router_ip, interface_name, ip_address, status, proto)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Saved current interface status for {router_ip}")


def notify_discord(router_ip, interface_name, ip_address, status, proto):
    discord_webhook = os.getenv("DISCORD_WEBHOOK")

    if not discord_webhook:
        print("No DISCORD_WEBHOOK found in environment")
        return

    message = (
        f"**Router Alert**\n"
        f"Router: `{router_ip}`\n"
        f"Interface: `{interface_name}`\n"
        f"IP: `{ip_address}`\n"
        f"Status: **{status} / {proto}**\n"
        f"Time: {datetime.now(THAI_TZ).strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )

    try:
        requests.post(discord_webhook, json={"content": message})
        print(f"Sent alert to Discord for {router_ip} - {interface_name}")
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")
