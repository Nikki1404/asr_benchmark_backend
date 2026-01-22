# ASR Benchmark Hub - Backend

This document provides a comprehensive overview of the Python backend for the ASR Benchmark Hub, built with FastAPI.

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [API Documentation (Swagger UI)](#api-documentation-swagger-ui)
- [API Endpoints Overview](#api-endpoints-overview)

## Overview

This backend serves as the backbone for the ASR Benchmark Hub frontend. It's a robust RESTful API that handles:
- **Data Persistence**: Storing and retrieving benchmark reports using a simple SQLite database.
- **Business Logic**: Processing uploaded data and preparing it for analysis.
- **Secure API Proxy**: Acting as a secure intermediary for all requests to the Google Gemini API, ensuring the API key is never exposed to the client.

## Tech Stack

- **FastAPI**: A modern, high-performance web framework for building APIs with Python.
- **Uvicorn**: A lightning-fast ASGI server, used to run the FastAPI application.
- **SQLAlchemy**: The Python SQL Toolkit and Object Relational Mapper (ORM) for all database interactions.
- **SQLite**: A simple, file-based SQL database engine.
- **Pydantic**: For data validation and settings management, ensuring data integrity.
- **Openpyxl**: A library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files.
- **Google Generative AI for Python**: The official Python SDK for the Gemini API.

## Features

- **RESTful API** for managing benchmark reports and data.
- **SQLite Database** for simple, file-based data persistence.
- **SQLAlchemy ORM** for elegant and efficient database interactions.
- **Secure Proxy** for all Google Gemini API calls, keeping the API key on the server.
- **Excel File Processing**: Endpoint to upload and parse `.xlsx` benchmark files.
- **Database Seeding**: Automatically populates the database with initial sample data on first startup.
- **Automatic Interactive API Docs**: Generated on-the-fly by FastAPI, with support for Swagger UI and ReDoc.

## Project Structure

```
backend/
├── api/                  # API routers/endpoints
│   ├── ai_services.py
│   ├── benchmarks.py
│   └── posts.py
├── crud.py               # Create, Read, Update, Delete database logic
├── database.py           # SQLAlchemy database engine setup
├── helpers.py            # Helper utility functions
├── main.py               # Main FastAPI application instance and startup logic
├── models.py             # SQLAlchemy ORM models (database tables)
├── requirements.txt      # Python dependencies
├── schemas.py            # Pydantic models for data validation and serialization
├── seed_data.py          # Initial data to seed the database
└── README.md             # This documentation file
```

## Setup Instructions

### 1. Prerequisites

- Python 3.8+
- `pip` (Python package installer)

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

The application uses an `.env` file to manage the Google Gemini API key securely.

1.  Rename the example file `.env.example` to `.env`.
2.  Open the new `.env` file and add your Gemini API key.

```
API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

The application will automatically load this key. **Do not commit the `.env` file to version control.**

### 5. Run the Server

Start the development server using `uvicorn`.

```bash
uvicorn main:app --reload
```

- `--reload` enables auto-reload, so the server will restart automatically when you make code changes.

The backend server will now be running at `http://127.0.0.1:8000`.

## API Documentation (Swagger UI)

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it in your browser:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

These interfaces allow you to explore and test all the available API endpoints directly, see the expected request bodies, and view response models.

## API Endpoints Overview

### Posts (`/api/posts`)

- `GET /`: Retrieves a list of all benchmark reports.
- `POST /`: Creates a new benchmark report. Expects post data in the request body.
- `GET /{id}`: Retrieves a single report by its unique ID.

### Benchmarks (`/api/benchmarks`)

- `POST /upload`: Uploads an Excel file (`.xlsx`). It parses the file and returns the structured benchmark data as JSON.

### AI Services (`/api/ai`)

These endpoints are proxies to the Google Gemini API.

- `POST /summarize`: Generates a concise summary of a given text content.
- `POST /generate-report`: Creates a full blog post (title, excerpt, content) from a JSON object containing benchmark statistics.
- `POST /analyze-errors`: Compares a ground truth string and a transcription string to identify and categorize errors (substitutions, deletions, insertions).
- `POST /compare-models`: Generates a detailed head-to-head analysis comparing the performance of two different models based on their benchmark data.
