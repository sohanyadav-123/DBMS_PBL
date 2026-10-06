# 🛡️ IT Helpdesk & Asset Support Management System

> A college DBMS project demonstrating database design, ER relationships, CRUD operations, SQL JOINs, and role-based access through a web interface.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Structure](#database-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the App](#running-the-app)
- [Demo Credentials](#demo-credentials)
- [SQL Concepts Demonstrated](#sql-concepts-demonstrated)
- [Team](#team)

---

## ✨ Features

| Portal | Capabilities |
|--------|-------------|
| 👤 **User** | Create tickets, view own tickets, track status |
| 🔧 **Technician** | View assigned tickets, update status, add resolution notes |
| ⚡ **Admin** | Full control — users, technicians, assets, categories, SLA policies, dashboard stats |

- Role-based access control (User / Technician / Admin)
- Asset management with warranty & status tracking
- SLA policy enforcement by ticket priority

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python 3, Flask
- **Database:** MySQL 8+
- **DB Driver:** `mysql-connector-python`
- **Auth:** Werkzeug password hashing

---

## 🗃️ Database Structure

```
Users        ──┐
Technicians  ──┤──► Tickets ◄── Categories
Assets       ──┘               SLA Policies
```

| Table | Relationships |
|-------|--------------|
| `users` | 1:N → `tickets` |
| `technicians` | 1:N → `tickets` |
| `assets` | 1:N → `tickets` |
| `categories` | 1:N → `tickets` |
| `tickets` | FK to users, technicians, assets, categories |

---

## ✅ Prerequisites

Make sure the following are installed before you start:

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.8 or higher | [python.org](https://www.python.org/downloads/) |
| MySQL Server | 8.0 or higher | [mysql.com](https://dev.mysql.com/downloads/mysql/) |
| Git | Any | [git-scm.com](https://git-scm.com/) |

> **Windows users:** During Python installation, tick ✅ **"Add Python to PATH"**.  
> **macOS users:** Python 3 can also be installed via `brew install python`.  
> **Linux users:** Use `sudo apt install python3 python3-pip python3-venv mysql-server` (Debian/Ubuntu).

---

## 🚀 Installation

### Step 1 — Clone the Repository

```bash
git clone <your-repo-url>
cd DBMS_pbl
```

---

### Step 2 — Set Up the MySQL Database

Start your MySQL service first:

<details>
<summary>▶ Windows</summary>

Open **Services** (search in Start Menu) → Start **MySQL80**, or run:
```cmd
net start MySQL80
```
Then import the database:
```cmd
mysql -u root -p < database.sql
```

</details>

<details>
<summary>▶ macOS</summary>

If installed via Homebrew:
```bash
brew services start mysql
```
Or via MySQL installer, open **System Preferences → MySQL → Start**.  
Then import:
```bash
mysql -u root -p < database.sql
```

</details>

<details>
<summary>▶ Linux (Ubuntu/Debian)</summary>

```bash
sudo systemctl start mysql
# or for older systems:
sudo service mysql start

mysql -u root -p < database.sql
```

</details>

---

### Step 3 — Create a Python Virtual Environment

<details>
<summary>▶ Windows (Command Prompt / PowerShell)</summary>

```cmd
python -m venv venv
venv\Scripts\activate
```

</details>

<details>
<summary>▶ macOS / Linux</summary>

```bash
python3 -m venv venv
source venv/bin/activate
```

</details>

You should see `(venv)` at the start of your terminal prompt when the environment is active.

---

### Step 4 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 5 — Configure Environment Variables

<details>
<summary>▶ Windows (Command Prompt)</summary>

```cmd
copy .env.example .env
```

</details>

<details>
<summary>▶ macOS / Linux</summary>

```bash
cp .env.example .env
```

</details>

Open `.env` in any text editor and fill in your MySQL credentials:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_root_password
DB_NAME=it_helpdesk
SECRET_KEY=any_random_string_here
```

---

## ▶️ Running the App

Make sure your virtual environment is active, then:

<details>
<summary>▶ Windows</summary>

```cmd
venv\Scripts\activate
python app.py
```

</details>

<details>
<summary>▶ macOS / Linux</summary>

```bash
source venv/bin/activate
python3 app.py
```

</details>

Then open your browser and go to:

```
http://127.0.0.1:5000
```

> **Port conflict?** If port 5000 is already in use (common on macOS due to AirPlay), either:
> - macOS: Go to **System Preferences → General → AirDrop & Handoff** → disable **AirPlay Receiver**
> - Or change the port: `python3 app.py` → edit the last line in `app.py` to `app.run(port=5001, debug=True)`

---

## 🔐 Demo Login Credentials

| Role | Email | Password |
|------|-------|----------|
| ⚡ Admin | `admin@company.com` | `admin123` |
| 🔧 Technician | `technician@company.com` | `tech123` |
| 👤 User | `user@company.com` | `user123` |

---

## 📐 SQL Concepts Demonstrated

| Concept | Where Used |
|---------|-----------|
| **JOINs** | Fetching ticket details with user names, asset tags, category names |
| **Aggregations** | `COUNT()` + `GROUP BY` for dashboard stats (tickets by status/priority) |
| **CRUD** | `INSERT`, `UPDATE`, `DELETE`, `SELECT` across all entities |
| **Foreign Keys** | `tickets` references `users`, `assets`, `technicians`, `categories` |
| **Hashed Passwords** | `werkzeug.security` bcrypt hashing — no plaintext passwords |
| **Role-based Access** | Session-based route guards by `role` column in `users` table |

---

## 👥 Team

| Name | Role |
|------|------|
| Sohan | Developer |
| Kiran | Developer |
| Ram | Developer |
| Rock | Developer |
| Alsabur | Developer |
| Soumya | Developer |
| Samyuktha | Developer |
| Abhinay | Developer |
| Tanush | Developer |
| Sriram | Developer |

---

## 🗂️ Project Structure

```
DBMS_pbl/
├── app.py                  # Flask backend & all API routes
├── database.sql            # Full DB schema + sample data
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
├── .env                    # Your local config (don't commit this!)
├── static/
│   ├── css/style.css       # Dark theme design system
│   └── js/                 # Per-page JavaScript (tickets, assets, etc.)
└── templates/              # Jinja2 HTML templates
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

> **DBMS Project — 2024** · Built with Flask + MySQL
