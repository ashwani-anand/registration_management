# Registration Management System

## Prerequisites
- Python 3.x
- PostgreSQL (or MySQL)

## Backend Setup
1. Install dependencies:
    ```bash
    pip install Flask Flask-SQLAlchemy psycopg2
    ```

2. Create a PostgreSQL database and configure the connection string in `app.py`:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/registration_db'
    ```

3. Run the Flask backend:
    ```bash
    python app.py
    ```

## Frontend Setup
Open `frontend/index.html` in your browser. The frontend will interact with the Flask API to perform CRUD operations.

## Notes
Ensure that the backend is running on `http://localhost:5000` before interacting with the frontend.
