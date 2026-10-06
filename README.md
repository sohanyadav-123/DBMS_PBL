# IT Helpdesk & Asset Support Management System

## Project Purpose
This is a college-level DBMS project designed to demonstrate database design, ER relationships, primary/foreign keys, CRUD operations, SQL JOINs, and overall database management through a web interface. The project implements a small company IT Helpdesk and Asset Support Management website.

## Features
- **User Portal:** Create IT support tickets, view own tickets, and track statuses.
- **Technician Portal:** View assigned tickets, update statuses, and add resolution notes.
- **Admin Portal:** Manage users, technicians, assets, categories, SLA policies, and view overall dashboard statistics.
- **Role-based Access:** Distinct dashboards and permissions for Users, Technicians, and Admins.
- **Asset Management:** Track hardware/software assets and their warranty/status.

## Technology Used
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Backend:** Python, Flask
- **Database:** MySQL 8+
- **Database Driver:** mysql-connector-python

## Database Structure & ER Relationships
The database consists of the following core entities:
- **Users (1:N Tickets)**
- **Technicians (1:N Tickets)**
- **Assets (1:N Tickets)**
- **Categories (1:N Tickets)**
- **SLA Policies**
- **Tickets** (Contains foreign keys to Users, Assets, Technicians, Categories)

## Installation Guide

### 1. Database Setup
1. Ensure MySQL server is installed and running.
2. Open your MySQL client (e.g., MySQL Workbench or CLI).
3. Run the SQL script to create the database and insert sample data:
   ```bash
   mysql -u root -p < database.sql
   ```

### 2. Python Environment Setup
1. Install Python 3.
2. It's recommended to create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Open `.env` and update `DB_PASSWORD` with your MySQL root password.

### 4. Running the Application
1. Start the Flask app:
   ```bash
   python app.py
   ```
2. Open your browser and go to `http://127.0.0.1:5000`

## Demo Login Credentials

All passwords are `admin123`, `tech123`, or `user123` respectively for their roles.

**Admin:**
- Email: `admin@company.com`
- Password: `admin123`

**Technician:**
- Email: `technician@company.com`
- Password: `tech123`

**User:**
- Email: `user@company.com`
- Password: `user123`

## Main SQL Queries Implemented
The project demonstrates various SQL queries such as:
- **JOINs:** Fetching ticket details along with user names, asset tags, and category names.
- **Aggregations:** Counting tickets by status, category, and priority using `COUNT()` and `GROUP BY`.
- **CRUD Operations:** `INSERT`, `UPDATE`, `DELETE`, and `SELECT` on all main entities.
