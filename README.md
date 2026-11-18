# B2B Analytics Engine

A secure, tenant-isolated backend API built with FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication.

Most backend tutorials just build basic CRUD apps where all users dump data into the same bucket. I built this microservice to solve the catastrophic risk of data leakage in Business-to-Business (B2B) SaaS environments by enforcing strict, database-level tenant isolation. 

Instead of a basic API, this engine acts as a secure multi-tenant vault—authenticating merchants, rejecting malformed payloads, and guaranteeing that a company can only ever query and ingest their own isolated data.

## Why I Built This (The Core Features)

* **Tenant Isolation:** Engineered strict data silos at the database layer. Every database query is cryptographically bound to the authenticated merchant's unique ID, preventing cross-tenant data exposure.
* **Production-Grade Auth:** Implemented full JWT login flows. Debugged and resolved underlying dependency clashes between `passlib` and modern `bcrypt` releases to ensure stable, enterprise-ready password hashing.
* **Enterprise Architecture:** Structured as a modular REST API using **FastAPI**. It uses Pydantic for strict data validation at the routing layer and SQLAlchemy 2.0 to securely map operations to a persistent PostgreSQL database.
* **Zero Trust Credentials:** Abstracted all environment variables, secret keys, and database URLs using `python-dotenv`, ensuring zero hardcoded credentials ever touch version control.

## Tech Stack

* **Backend:** FastAPI, Python 3.x
* **Database & ORM:** PostgreSQL, SQLAlchemy 2.0
* **Authentication & Security:** JSON Web Tokens (JWT) via `python-jose`, `passlib`, `bcrypt`
* **Validation & Environment:** Pydantic, `python-dotenv`

## Architecture Breakdown

I designed this project with scalability and clean code principles in mind. The logic is strictly separated:

* `main.py` - The FastAPI traffic controller and API routing logic.
* `auth.py` - Cryptographic hashing, password verification, and JWT token generation.
* `schemas.py` - Pydantic models acting as the strict data bouncer for incoming API requests.
* `models.py` & `database.py` - SQLAlchemy database mapping and secure session management.

## How to Run It Locally

**1. Clone the repository**

git clone [https://github.com/YOUR_USERNAME/b2b-analytics-engine.git](https://github.com/YOUR_USERNAME/b2b-analytics-engine.git) 
cd b2b-analytics-engine

**2. Set up the virtual environment & install dependencies**

python -m venv env
source env/Scripts/activate  # On Windows use: env\Scripts\activate
pip install fastapi[all] sqlalchemy psycopg2-binary python-jose[cryptography] passlib bcrypt==3.2.2 python-dotenv
*(Note: bcrypt is explicitly pinned to v3.2.2 to ensure passlib compatibility).*

**3. Configure Environment Variables** 
Create a `.env` file in the root directory and add your local PostgreSQL credentials and a secure secret key:

DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/b2b_ecommerce
SECRET_KEY=generate_a_random_secure_string_here


**4. Start the FastAPI Backend**

uvicorn app.main:app --reload
*The API will be live at http://127.0.0.1:8000. You can view the interactive Swagger UI docs at http://127.0.0.1:8000/docs.*

## Next Steps & Roadmap

* Building out the raw data ingestion pipelines for the `sales_records` tables.
* Writing a comprehensive `pytest` suite for automated endpoint verification.
* Containerizing the application using Docker Compose for seamless cloud deployment.
