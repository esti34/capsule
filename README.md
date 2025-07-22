# FastAPI + React TypeScript Project

This project consists of a FastAPI backend and React TypeScript frontend.

## Project Structure

- `backend/`: FastAPI application
- `frontend/`: React TypeScript application

## Backend Setup

The backend is built with FastAPI, SQLAlchemy, and Pydantic.

### Installation

```bash
pip install fastapi uvicorn[standard] sqlalchemy pydantic
```

### Running the Backend

```bash
cd backend
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Frontend Setup

The frontend is built with React and TypeScript.

### Installation

```bash
cd frontend
npm install
```

### Running the Frontend

```bash
cd frontend
npm start
```

The React app will be available at http://localhost:3000

## Features

- User management (create/list users)
- Item management (create/list items)
- RESTful API with FastAPI
- React hooks for state management
- TypeScript for type safety 