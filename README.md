# IT Helpdesk & Asset Support Management System

> A web-based IT support ticket and asset lifecycle management system built as a DBMS course project.

| Field | Details |
|---|---|
| **Student Name** | Dasuri Sohan Yadav |
| **Roll Number** | 25WU0102269 |
| **Project Title** | IT Helpdesk & Asset Support Management System |
| **Course** | Database Management Systems (DBMS Course Project) |

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Design](#database-design)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Login Credentials](#login-credentials)
- [Project Structure](#project-structure)
- [SQL Concepts Used](#sql-concepts-used)
- [Project Deliverables & Presentations](#project-deliverables--presentations)

---

## Features

| Portal | Capabilities |
|--------|-------------|
| 👤 **User** | Raise support tickets, track ticket status, view history |
| 🔧 **Technician** | View assigned tickets, update status, add resolution notes |
| ⚙️ **Admin** | Manage users, technicians, assets, categories, SLA policies; view dashboard statistics |

- Secure role-based authentication (Admin / Technician / User)
- Asset tracking with purchase date, warranty, and status
- SLA enforcement by ticket priority (High / Medium / Low)
- Logout confirmation dialog to prevent accidental sign-out
- Toast notifications for form feedback

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, Flask |
| Database | MySQL 8+ |
| DB Driver | mysql-connector-python |
| Auth | Werkzeug password hashing (scrypt) |

---

## Database Design

```
users         ──┐
technicians   ──┤──► tickets ◄── categories
assets        ──┘               sla_policies
```

| Table | Key Relationships |
|-------|------------------|
| `users` | One user → many tickets |
| `technicians` | One technician → many tickets |
| `assets` | One asset → many tickets |
| `categories` | One category → many tickets |
| `tickets` | Foreign keys to users, technicians, assets, categories |
| `sla_policies` | Defines response & resolution time by priority |

---

## Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.8+ | [python.org](https://www.python.org/downloads/) |
| MySQL Server | 8.0+ | [mysql.com](https://dev.mysql.com/downloads/mysql/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

> **Windows:** During Python installation, enable **"Add Python to PATH"**.  
> **macOS:** Install Python via `brew install python` or the official installer.  
> **Linux (Debian/Ubuntu):** `sudo apt install python3 python3-pip python3-venv mysql-server`

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd DBMS_pbl
```

---

### 2. Start MySQL and import the database

<details>
<summary>Windows</summary>

```cmd
net start MySQL80
mysql -u root -p < database.sql
```

</details>

<details>
<summary>macOS</summary>

```bash
brew services start mysql
mysql -u root -p < database.sql
```

</details>

<details>
<summary>Linux</summary>

```bash
sudo systemctl start mysql
mysql -u root -p < database.sql
```

</details>

---

### 3. Create a virtual environment

<details>
<summary>Windows</summary>

```cmd
python -m venv venv
venv\Scripts\activate
```

</details>

<details>
<summary>macOS / Linux</summary>

```bash
python3 -m venv venv
source venv/bin/activate
```

</details>

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Set up environment variables

<details>
<summary>Windows</summary>

```cmd
copy .env.example .env
```

</details>

<details>
<summary>macOS / Linux</summary>

```bash
cp .env.example .env
```

</details>

Edit `.env` and fill in your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=it_helpdesk
SECRET_KEY=any_random_secret_string
```

---

## Running the Application

Ensure the virtual environment is active, then:

<details>
<summary>Windows</summary>

```cmd
python app.py
```

</details>

<details>
<summary>macOS / Linux</summary>

```bash
python3 app.py
```

</details>

Open your browser and visit:

```
http://127.0.0.1:5001
```

> **Port conflict on macOS?** Disable **AirPlay Receiver** in System Preferences → General → AirDrop & Handoff, or change the port in the last line of `app.py` to another port number.

---

## Login Credentials

The following demo accounts are pre-loaded by `database.sql`:

| Role | Email | Password |
|------|-------|----------|
| Admin | `sohan@company.com` | `admin123` |
| Technician | `technician@company.com` | `tech123` |
| User | `kiran@company.com` | `user123` |

All user accounts use the password `user123`. All technician accounts use `tech123`.

---

## Project Structure

```
DBMS_pbl/
├── Presentation-I/
│   └── IT_Helpdesk_Asset_DBMS_0111.pptx            # Presentation 1: System overview & requirements
├── Presentation-II/
│   └── DBMS_ER_Schema_Query_Presentation_0222.pptx # Presentation 2: ER schema & SQL queries
├── Presentation-III/                               # Presentation 3 (final demonstration slides)
├── Project-Report/                                 # Final DBMS project report & documentation
├── app.py                                          # Flask application — all routes and API endpoints
├── database.sql                                    # Database schema and sample data
├── requirements.txt                                # Python dependencies
├── .env.example                                    # Environment variable template
├── .env                                            # Local configuration (do not commit)
├── static/
│   ├── css/style.css                               # Application stylesheet
│   └── js/                                         # JavaScript — main.js, dashboard.js, tickets.js, assets.js
└── templates/                                      # Jinja2 HTML templates
    ├── login.html
    ├── admin_dashboard.html
    ├── technician_dashboard.html
    ├── user_dashboard.html
    ├── tickets.html
    ├── ticket_details.html
    ├── assets.html
    ├── users.html
    ├── technicians.html
    ├── categories.html
    └── sla_policies.html
```

---

## SQL Concepts Used

| Concept | Usage |
|---------|-------|
| **Joins** | Ticket list queries combining users, assets, categories, technicians |
| **Aggregation** | `COUNT()` with `GROUP BY` for dashboard statistics |
| **CRUD** | Full create, read, update, delete across all entities |
| **Foreign Keys** | `tickets` references four separate tables |
| **Password Hashing** | Werkzeug scrypt hashing — no plaintext passwords stored |
| **Role-based Access** | Session checks on every protected route |
| **Subqueries / Filters** | Filtered ticket views per user role |

---

## Project Deliverables & Presentations

| Folder / File | Description |
|---|---|
| `Presentation-I/` | **Presentation 1:** System overview, problem statement, user roles, system architecture (`IT_Helpdesk_Asset_DBMS_0111.pptx`) |
| `Presentation-II/` | **Presentation 2:** Entity-Relationship (ER) model, schema design, normalization, SQL queries (`DBMS_ER_Schema_Query_Presentation_0222.pptx`) |
| `Presentation-III/` | **Presentation 3:** Final project presentation and live demonstration |
| `Project-Report/` | Complete project documentation and final report |

---

> DBMS Project — 2024 · Built with Flask and MySQL
