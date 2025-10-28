# ipa-project
IPA-Project

# === MySQL ===
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=ipa2025
MYSQL_USER=root
MYSQL_PASSWORD=rootpassword

# === Flask ===
DB_HOST=mysql
DB_USER=root
DB_PASSWORD=rootpassword
DB_NAME=ipa2025

# === Ports ===
WEB_PORT=8080
MYSQL_PORT=3306

# == Command ==
docker compose up --build --detach
docker compose down