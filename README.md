B2B Analytics Engine
A secure, tenant-isolated backend API designed to handle merchant authentication, data validation, and core B2B analytics.

Instead of just building another CRUD app, I engineered this MVP to treat security and data integrity as first-class citizens from day one. It is built to withstand real-world edge cases—from strict Pydantic payload validation to handling cryptographic dependency alignments and environment-level secret management.

Tech Stack
Framework: FastAPI (Python)

Database: PostgreSQL & SQLAlchemy (ORM)

Authentication: JWT (JSON Web Tokens) via python-jose

Security: passlib with bcrypt (strictly calibrated for dependency stability)

Environment Management: python-dotenv

Core Features
Isolated Tenant Architecture: Merchant data is securely siloed. Every analytical request and database query is bound to the authenticated merchant's specific ID.

Production-Grade Auth: Complete JWT login flow with securely hashed passwords. Hardcoded credentials are strictly prohibited; all secrets are managed via isolated .env environments.

Aggressive Data Validation: Pydantic acts as a strict bouncer at the routing layer, intercepting malformed payloads (like missing company_name fields) and returning explicit 422 errors before they can hit the database.

Local Setup & Quick Start
1. Clone the repository


git clone https://github.com/YOUR_USERNAME/b2b-analytics-engine.git
cd b2b-analytics-engine
2. Set up the virtual environment & install dependencies


python -m venv env
source env/Scripts/activate  # Windows
pip install fastapi[all] sqlalchemy psycopg2-binary python-jose[cryptography] passlib bcrypt==3.2.2 python-dotenv
(Note: bcrypt is explicitly pinned to v3.2.2 to ensure passlib compatibility).

3. Configure Environment Variables
Create a .env file in the root directory (this file is git-ignored for security). Add your local PostgreSQL credentials and a secure secret key:

Code snippet
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/b2b_ecommerce
SECRET_KEY=generate_a_random_secure_string_here
4. Run the Server


uvicorn app.main:app --reload
The API will be live at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can access the interactive Swagger documentation by navigating to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

What's Next
This MVP sets the foundation. The immediate next phases include building out the raw data ingestion pipelines for the sales_records tables, writing a Pytest suite for automated endpoint verification, and containerizing the application with Docker Compose for seamless cloud deployment.
