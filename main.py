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
def db_connect(
    host: str = None,
    port: int = None,
    user: str = None,
    password: str = None,
    database: str = None,
):
    try:
        # Use provided parameters or fall back to config
        if host is None:
            cfg = load_config()
            host = cfg["host"]
            port = cfg["port"]
            user = cfg["user"]
            password = cfg["password"]
            database = cfg["database"]
        
        # Create connection with parameters
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connection_timeout=5,
        )
        conn.close()
        return {
            "status":  "success",
            "message": "Connected to MySQL successfully",
            "host":    host,
            "port":    port,
            "user":    user,
            "database": database,
        }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"DB connection failed: {e}")


# ── 3. DB Data ────────────────────────────────────────────────────────────────
@app.get("/db_data")
def db_data(
    host: str = None,
    port: int = None,
    user: str = None,
    password: str = None,
    database: str = None,
    table: str = None,
):
    try:
        # Use provided parameters or fall back to config
        if host is None:
            cfg = load_config()
            host = cfg["host"]
            port = cfg["port"]
            user = cfg["user"]
            password = cfg["password"]
            database = cfg["database"]
        
        # Create connection with parameters
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connection_timeout=5,
        )
        cursor = conn.cursor(dictionary=True)
        
        # If table is specified, fetch all rows from that table
        if table:
            cursor.execute(f"SELECT * FROM {table};")
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return {
                "status":  "success",
                "table":   table,
                "rows":    rows,
                "count":   len(rows),
                "database": database,
            }
        else:
            # If no table specified, show all databases
            cursor.execute("SHOW DATABASES;")
            databases = [row["Database"] if isinstance(row, dict) else row[0] for row in cursor.fetchall()]
            cursor.close()
            conn.close()
            return {
                "status":    "success",
                "databases": databases,
                "count":     len(databases),
            }
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {e}")
