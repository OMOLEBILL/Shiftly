# Shiftly

Shiftly is a **shift scheduling MVP** designed to allocate employees (who Shiftly refers to as talents) to shifts efficiently while respecting availability and constraints. The project separates responsibilities clearly, applies abstraction for flexibility, and uses adapters for data transformation.

> ⚠️ **Note:** This is an MVP (not yet in production). Future enhancements may include maximum hours validation, consecutive-day checks, night-to-morning shift restrictions, and employee request handling.

---

## Features

- Fetch talent and shift data from a PostgreSQL database.
- Filter talents based on availability and constraints.
- Convert raw data into **Pandas DataFrames** for easy manipulation.
- Apply **eligibility rules** to determine which talents can work which shifts.
- Allocate shifts using a **rule-based system**.
- Output scheduled assignments.

> ⚠️ **Note:** Future enhancements will include:

- Maximum hours validation.
- Consecutive-day checks.
- Night-to-morning shift restrictions.
- Employee request handling.
- Applying AI models to predict staffing needs based on external factors

---

## Setup

Follow these instructions to get Shiftly running locally.
### 1. Clone the repository

```bash
git clone https://github.com/your-username/shiftly.git
cd shiftly
```

### 2. Create a virtual environment (optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the environment variables

Create a .env file in the root of the project

```bash
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### 5. Set up the database

- Connect to your postgreSQL database
- Run the schema file to create tables and views needed for shiftly

```bash
psql -U your_user -d your_db -f schema.sql
```

- Seed the database with imaginary data

```bash
psql -U your_user -d your_db -f seed.sql
```

### 6. Run the demo

```bash
python3 -m app.demo.demo
```