from fastapi import FastAPI
from datetime import datetime
import socket
import aiomysql

app = FastAPI(title="App1", version="1.0.0")

# MySQL connection pool
mysql_pool = None

@app.on_event("startup")
async def startup():
    global mysql_pool
    mysql_pool = await aiomysql.create_pool(
        host='mysql-service',  # Kubernetes DNS
        port=3306,
        user='root',
        password='root',  # Replace with actual password
        minsize=1,
        maxsize=10
    )

@app.on_event("shutdown")
async def shutdown():
    global mysql_pool
    mysql_pool.close()
    await mysql_pool.wait_closed()


@app.get("/health")
def health():
    return {"status": "ok", "app": "app1"}


@app.get("/info")
def info():
    return {
        "app": "app1",
        "server": socket.gethostname(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/databases")
async def get_databases():
    """Get list of all MySQL databases"""
    async with mysql_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SHOW DATABASES;")
            result = await cursor.fetchall()
            databases = [db[0] for db in result]
    
    return {
        "app": "app1",
        "databases": databases,
        "count": len(databases),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/tables/{database_name}")
async def get_tables(database_name: str):
    """Get all tables in a specific database"""
    async with mysql_pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(f"USE {database_name};")
            await cursor.execute("SHOW TABLES;")
            result = await cursor.fetchall()
            tables = [table[0] for table in result]
    
    return {
        "app": "app1",
        "database": database_name,
        "tables": tables,
        "count": len(tables),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@app.get("/call-app2-info")
async def call_app2_info():
    """Call app2's /info endpoint from app1"""
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://app2-svc/info",
            timeout=10.0
        )
        return response.json()