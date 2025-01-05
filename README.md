# FastAPI CRUD with PostgreSQL

This project is a simple FastAPI application that implements CRUD (Create, Read, Update, Delete) operations using PostgreSQL as the database. The app uses **SQLAlchemy** for database schema definition, **databases** for asynchronous database access, and **Pydantic** for data validation. Configuration is managed using environment variables loaded from a `.env` file.

---

## Features

- **GET /users**: Retrieve all users from the database.
- **POST /users**: Add a new user to the database.
- **PUT /users**: Update an existing user in the database.
- **DELETE /users/{user_id}**: Delete a user by their ID.

---

## Requirements

- Python 3.9+
- PostgreSQL

### Python Dependencies

The required dependencies can be installed via `pip`. See the installation section below for more details.

- **FastAPI**: Framework for building APIs.
- **SQLAlchemy**: ORM for defining database schema.
- **databases**: Library for asynchronous database access.
- **Pydantic**: Data validation and serialization.
- **python-dotenv**: Load environment variables from a `.env` file.
- **asyncpg**: Asynchronous PostgreSQL client.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sebakrys/FastAPI_CRUD.git
cd FastAPI_CRUD
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the project root and add your database configuration:

```
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
```
Replace `<username>`, `<password>`, and `<database_name>` with your PostgreSQL credentials.

---

## Running the Application

Start the FastAPI server using Uvicorn:
```bash
uvicorn app:app --reload
```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

### Interactive API Documentation
- Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.
- Open [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) for ReDoc.

---

## Database Setup

Before running the application, ensure your PostgreSQL database is set up. You can also create the table manually, but this is optional as it will be automatically created if it does not exist. To create the table manually, use the following SQL command:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
);
```

---

## API Endpoints

### **GET /users**
Retrieve all users from the database.

**Response:**
```json
[
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    },
    {
        "id": 2,
        "name": "Jane Smith",
        "email": "jane.smith@example.com"
    }
]
```

### **POST /users**
Add a new user.

**Request Body:**
```json
{
    "name": "Jane Doe",
    "email": "jane@example.com"
}
```

**Response:**
```json
{
    "id": 2,
    "name": "Jane Doe",
    "email": "jane@example.com"
}
```

### **PUT /users**
Update an existing user.

**Request Body:**
```json
{
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@example.com"
}
```

**Response:**
```json
{
    "id": 1,
    "name": "John Smith",
    "email": "john.smith@example.com"
}
```

### **DELETE /users/{user_id}**
Delete a user by ID.

**Response:**
```json
{
    "message": "User deleted successfully"
}
```

---

## Testing

You can use tools like **Postman** or **cURL** to test the API endpoints.

Example `cURL` commands:

- **GET Users:**
  ```bash
  curl -X GET http://127.0.0.1:8000/users
  ```

- **POST User:**
  ```bash
  curl -X POST http://127.0.0.1:8000/users \
       -H "Content-Type: application/json" \
       -d '{"name": "Alice", "email": "alice@example.com"}'
  ```

- **PUT User:**
  ```bash
  curl -X PUT http://127.0.0.1:8000/users \
       -H "Content-Type: application/json" \
       -d '{"id": 1, "name": "Alice Smith", "email": "alice.smith@example.com"}'
  ```

- **DELETE User:**
  ```bash
  curl -X DELETE http://127.0.0.1:8000/users/1
  ```

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Acknowledgments

This project was inspired by the need to build a simple, clean API for managing users with FastAPI and PostgreSQL. Special thanks to the FastAPI and SQLAlchemy communities for their excellent documentation and tools.

