# PostgreSQL Setup for Project

This guide will help you set up PostgreSQL for this project.

## Prerequisites

1. Install PostgreSQL from the [official website](https://www.postgresql.org/download/)
2. Make sure PostgreSQL is running on your machine

## Configuration

The project uses the following default PostgreSQL configuration:
- **Username**: postgres
- **Password**: postgres
- **Host**: localhost
- **Port**: 5432
- **Database**: hacaton_db

## Setting up environment variables

You can override the default configuration by setting environment variables:

### Windows
```
set DB_USER=your_username
set DB_PASSWORD=your_password
set DB_HOST=your_host
set DB_PORT=your_port
set DB_NAME=your_database
```

### Linux/Mac
```
export DB_USER=your_username
export DB_PASSWORD=your_password
export DB_HOST=your_host
export DB_PORT=your_port
export DB_NAME=your_database
```

## Database Initialization

The application will automatically create the database if it doesn't exist when you run:

```
python run_backend.py
```

## Manual Database Setup

If you prefer to create the database manually, use the following commands:

1. Connect to PostgreSQL:
```
psql -U postgres
```

2. Create the database:
```
CREATE DATABASE hacaton_db;
```

3. Verify the database was created:
```
\l
```

4. Exit psql:
```
\q
```

## Troubleshooting

If you encounter issues with PostgreSQL connection:

1. Verify PostgreSQL is running
2. Ensure your credentials are correct
3. Check that the database exists
4. Make sure you have network access to the PostgreSQL server
5. Verify that pg_hba.conf is configured to allow your connection 