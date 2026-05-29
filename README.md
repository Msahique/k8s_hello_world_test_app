# k8s_hello_world_test_app
This repo contains the test app for k8s testing

## API Documentation

### Base URL
```
http://localhost:8000
```

### Available Endpoints

---

#### 1. Health Check
**Endpoint:** `GET /health`

**Description:** Check if the server is running.

**Parameters:** None

**Response:**
```json
{
  "message": "Hello, this server is running"
}
```

**Example:**
```
GET /health
```

---

#### 2. Database Connection
**Endpoint:** `GET /db_connect`

**Description:** Test database connection with optional custom connection parameters. If no parameters are provided, uses credentials from `config.ini`.

**Parameters (all optional):**
| Parameter | Type | Description |
|-----------|------|-------------|
| host | string | Database host (default: 127.0.0.1) |
| port | integer | Database port (default: 3306) |
| user | string | Database user (default: root) |
| password | string | Database password |
| database | string | Database name |

**Response:**
```json
{
  "status": "success",
  "message": "Connected to MySQL successfully",
  "host": "localhost",
  "port": 3306,
  "user": "root",
  "database": "mysql"
}
```

**Examples:**

Using default config:
```
GET /db_connect
```

Using custom parameters:
```
GET /db_connect?host=192.168.1.100&port=3306&user=root&password=Admin@1234&database=testdb
```

Partial parameters (override specific settings):
```
GET /db_connect?host=remote-db.example.com&database=production
```

---

#### 3. Database Data
**Endpoint:** `GET /db_data`

**Description:** Fetch database information or retrieve all rows from a specified table. If no table is specified, returns all databases. If a table is specified, returns all rows from that table with custom connection parameters.

**Parameters (all optional):**
| Parameter | Type | Description |
|-----------|------|-------------|
| host | string | Database host (default: 127.0.0.1) |
| port | integer | Database port (default: 3306) |
| user | string | Database user (default: root) |
| password | string | Database password |
| database | string | Database name |
| table | string | Table name to fetch data from |

**Response (List databases):**
```json
{
  "status": "success",
  "databases": ["information_schema", "mysql", "performance_schema", "testdb"],
  "count": 4
}
```

**Response (Fetch table data):**
```json
{
  "status": "success",
  "table": "users",
  "rows": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com"
    },
    {
      "id": 2,
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ],
  "count": 2,
  "database": "testdb"
}
```

**Examples:**

List all databases (default):
```
GET /db_data
```

Fetch all rows from a specific table:
```
GET /db_data?host=localhost&port=3306&user=root&password=Admin@1234&database=testdb&table=users
```

Fetch from custom connection with table name:
```
GET /db_data?host=remote-db.example.com&database=production&table=orders
```

---

### Error Responses

All endpoints return HTTP 500 with error details if a database error occurs:

```json
{
  "detail": "DB connection failed: [error message]"
}
```

---

### Running the Application

#### Local Development
```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

#### Docker
```bash
docker build -t hello_world:latest .
docker run -p 8000:8000 hello_world:latest
```

#### With Docker Compose
```bash
docker-compose up
```

---

### Configuration

Edit `config.ini` to set default database credentials:

```ini
[database]
host = 127.0.0.1
port = 3306
user = root
password = Admin@1234
database = mysql
```

---

### Requirements
- Python 3.7+
- FastAPI
- uvicorn
- mysql-connector-python
