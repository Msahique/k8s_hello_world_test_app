from fastapi import FastAPI, HTTPException
import mysql.connector
import configparser
import os

app = FastAPI(title="MySQL FastAPI", version="1.0.0")

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.ini")


def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return {
        "host":     config.get("database", "host"),
        "port":     config.getint("database", "port"),
        "user":     config.get("database", "user"),
        "password": config.get("database", "password"),
        "database": config.get("database", "database"),
    }


def get_connection():
    cfg = load_config()
    return mysql.connector.connect(
        host=cfg["host"],
        port=cfg["port"],
        user=cfg["user"],
        password=cfg["password"],
        database=cfg["database"],
        connection_timeout=5,
    )


# ── 1. Health ────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"message": "Hello, this server is running"}


# ── 2. DB Connect ─────────────────────────────────────────────────────────────
@app.get("/db_connect")
def db_connect():
    try:
        cfg = load_config()
        conn = get_connection()
        conn.close()
        return {
            "status":  "success",
            "message": "Connected to MySQL successfully",
            "host":    cfg["host"],
            "port":    cfg["port"],
            "user":    cfg["user"],
            "database": cfg["database"],
        }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")


# ── 3. DB Data ────────────────────────────────────────────────────────────────
@app.get("/db_data")
def db_data():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES;")
        databases = [row[0] for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return {
            "status":    "success",
            "databases": databases,
            "count":     len(databases),
        }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch databases: {e}")
