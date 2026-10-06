import os
from flask import Flask, render_template, request, redirect, url_session, session, jsonify, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default_secret_key')

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'it_helpdesk')
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# ----- ROUTES FOR PAGES -----

@app.route('/')
def index():
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect('/admin_dashboard')
        elif session.get('role') == 'technician':
            return redirect('/technician_dashboard')
        else:
            return redirect('/user_dashboard')
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection failed", "error")
            return render_template('login.html')
            
        cursor = conn.cursor(dictionary=True)
        
        # Check in users table
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            session['role'] = user['role']
            cursor.close()
            conn.close()
            if user['role'] == 'admin':
                return redirect('/admin_dashboard')
            return redirect('/user_dashboard')
            
        # Check in technicians table
        cursor.execute("SELECT * FROM technicians WHERE email = %s", (email,))
        tech = cursor.fetchone()
        
        if tech and check_password_hash(tech['password'], password):
            session['user_id'] = tech['technician_id']
            session['name'] = tech['name']
            session['role'] = 'technician'
            cursor.close()
            conn.close()
            return redirect('/technician_dashboard')
            
        cursor.close()
        conn.close()
        flash("Invalid email or password", "error")
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# Admin Routes
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('admin_dashboard.html')

@app.route('/users')
def users_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('users.html')

@app.route('/technicians')
def technicians_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('technicians.html')

@app.route('/assets')
def assets_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('assets.html')

@app.route('/categories')
def categories_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('categories.html')

@app.route('/sla_policies')
def sla_policies_page():
    if session.get('role') != 'admin':
        return redirect('/')
    return render_template('sla_policies.html')

# User & Tech Routes
@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') != 'user':
        return redirect('/')
    return render_template('user_dashboard.html')

@app.route('/technician_dashboard')
def technician_dashboard():
    if session.get('role') != 'technician':
        return redirect('/')
    return render_template('technician_dashboard.html')

@app.route('/tickets')
def tickets_page():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('tickets.html')

@app.route('/ticket_details/<int:id>')
def ticket_details(id):
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('ticket_details.html', ticket_id=id)

# ----- API ENDPOINTS -----

@app.route('/api/stats/dashboard')
def api_dashboard_stats():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    role = session.get('role')
    user_id = session['user_id']
    
    stats = {}
    
    if role == 'admin':
        cursor.execute("SELECT COUNT(*) as count FROM users")
        stats['total_users'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM technicians")
        stats['total_technicians'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM assets")
        stats['total_assets'] = cursor.fetchone()['count']
        cursor.execute("SELECT COUNT(*) as count FROM tickets")
        stats['total_tickets'] = cursor.fetchone()['count']
        
        cursor.execute("SELECT status, COUNT(*) as count FROM tickets GROUP BY status")
        ticket_status = {row['status']: row['count'] for row in cursor.fetchall()}
        stats['tickets_open'] = ticket_status.get('Open', 0)
        stats['tickets_in_progress'] = ticket_status.get('In Progress', 0)
        stats['tickets_resolved'] = ticket_status.get('Resolved', 0) + ticket_status.get('Closed', 0)
        
        cursor.execute("SELECT status, COUNT(*) as count FROM assets GROUP BY status")
        asset_status = {row['status']: row['count'] for row in cursor.fetchall()}
        stats['assets_available'] = asset_status.get('Available', 0)
        stats['assets_assigned'] = asset_status.get('Assigned', 0)
        stats['assets_maintenance'] = asset_status.get('Maintenance', 0)
        
    elif role == 'technician':
        cursor.execute("SELECT status, COUNT(*) as count FROM tickets WHERE technician_id = %s GROUP BY status", (user_id,))
        ticket_status = {row['status']: row['count'] for row in cursor.fetchall()}
        stats['assigned_tickets'] = sum(ticket_status.values())
        stats['open_tickets'] = ticket_status.get('Open', 0)
        stats['in_progress_tickets'] = ticket_status.get('In Progress', 0)
        stats['resolved_tickets'] = ticket_status.get('Resolved', 0) + ticket_status.get('Closed', 0)
        
    else: # user
        cursor.execute("SELECT status, COUNT(*) as count FROM tickets WHERE user_id = %s GROUP BY status", (user_id,))
        ticket_status = {row['status']: row['count'] for row in cursor.fetchall()}
        stats['total_tickets'] = sum(ticket_status.values())
        stats['open_tickets'] = ticket_status.get('Open', 0)
        stats['in_progress_tickets'] = ticket_status.get('In Progress', 0)
        stats['resolved_tickets'] = ticket_status.get('Resolved', 0) + ticket_status.get('Closed', 0)
        
    cursor.close()
    conn.close()
    return jsonify(stats)

@app.route('/api/tickets', methods=['GET', 'POST'])
def api_tickets():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        role = session.get('role')
        user_id = session['user_id']
        
        query = """
            SELECT t.*, u.name as user_name, a.asset_tag, c.name as category_name, tech.name as technician_name
            FROM tickets t
            LEFT JOIN users u ON t.user_id = u.user_id
            LEFT JOIN assets a ON t.asset_id = a.asset_id
            LEFT JOIN categories c ON t.category_id = c.category_id
            LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
        """
        
        if role == 'user':
            query += " WHERE t.user_id = %s ORDER BY t.created_at DESC"
            cursor.execute(query, (user_id,))
        elif role == 'technician':
            query += " WHERE t.technician_id = %s ORDER BY t.created_at DESC"
            cursor.execute(query, (user_id,))
        else:
            query += " ORDER BY t.created_at DESC"
            cursor.execute(query)
            
        tickets = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tickets)
        
    elif request.method == 'POST':
        if session.get('role') != 'user' and session.get('role') != 'admin':
            return jsonify({"error": "Only users can create tickets"}), 403
            
        data = request.json
        user_id = session['user_id']
        if session.get('role') == 'admin' and 'user_id' in data:
            user_id = data['user_id']
            
        try:
            cursor.execute("""
                INSERT INTO tickets (user_id, asset_id, category_id, priority, description)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_id,
                data.get('asset_id') or None,
                data['category_id'],
                data.get('priority', 'Medium'),
                data['description']
            ))
            conn.commit()
            ticket_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return jsonify({"message": f"Ticket #T{ticket_id:03d} created successfully.", "ticket_id": ticket_id})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/api/tickets/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def api_ticket(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("""
            SELECT t.*, u.name as user_name, u.email as user_email, u.department, 
                   a.asset_tag, c.name as category_name, tech.name as technician_name
            FROM tickets t
            LEFT JOIN users u ON t.user_id = u.user_id
            LEFT JOIN assets a ON t.asset_id = a.asset_id
            LEFT JOIN categories c ON t.category_id = c.category_id
            LEFT JOIN technicians tech ON t.technician_id = tech.technician_id
            WHERE t.ticket_id = %s
        """, (id,))
        ticket = cursor.fetchone()
        cursor.close()
        conn.close()
        if not ticket:
            return jsonify({"error": "Ticket not found"}), 404
        return jsonify(ticket)
        
    elif request.method == 'PUT':
        data = request.json
        role = session.get('role')
        
        # Build update query based on role
        updates = []
        params = []
        
        if 'status' in data:
            updates.append("status = %s")
            params.append(data['status'])
        
        if 'resolution' in data and role in ['technician', 'admin']:
            updates.append("resolution = %s")
            params.append(data['resolution'])
            
        if 'technician_id' in data and role == 'admin':
            updates.append("technician_id = %s")
            params.append(data['technician_id'] or None)
            
        if not updates:
            return jsonify({"message": "No valid fields to update"}), 400
            
        query = f"UPDATE tickets SET {', '.join(updates)} WHERE ticket_id = %s"
        params.append(id)
        
        try:
            cursor.execute(query, tuple(params))
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"message": "Ticket updated successfully"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/api/assets', methods=['GET', 'POST'])
def api_assets():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'GET':
        cursor.execute("SELECT * FROM assets ORDER BY asset_id DESC")
        assets = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(assets)
        
    elif request.method == 'POST':
        if session.get('role') != 'admin':
            return jsonify({"error": "Only admins can add assets"}), 403
            
        data = request.json
        try:
            cursor.execute("""
                INSERT INTO assets (asset_tag, type, serial_no, purchase_date, warranty_end, status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                data['asset_tag'], data['type'], data.get('serial_no'), 
                data.get('purchase_date'), data.get('warranty_end'), data.get('status', 'Available')
            ))
            conn.commit()
            asset_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return jsonify({"message": "Asset added successfully", "asset_id": asset_id})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/api/assets/<int:id>', methods=['PUT', 'DELETE'])
def api_asset(id):
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 401
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if request.method == 'PUT':
        data = request.json
        try:
            cursor.execute("""
                UPDATE assets 
                SET asset_tag=%s, type=%s, serial_no=%s, purchase_date=%s, warranty_end=%s, status=%s
                WHERE asset_id=%s
            """, (
                data['asset_tag'], data['type'], data.get('serial_no'), 
                data.get('purchase_date'), data.get('warranty_end'), data.get('status'), id
            ))
            conn.commit()
            return jsonify({"message": "Asset updated successfully"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400
            
    elif request.method == 'DELETE':
        try:
            cursor.execute("DELETE FROM assets WHERE asset_id=%s", (id,))
            conn.commit()
            return jsonify({"message": "Asset deleted successfully"})
        except Exception as e:
            conn.rollback()
            return jsonify({"error": str(e)}), 400

@app.route('/api/categories', methods=['GET'])
def api_categories():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM categories")
    categories = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(categories)

@app.route('/api/technicians', methods=['GET'])
def api_technicians():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT technician_id, name, specialization, email FROM technicians")
    techs = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(techs)

@app.route('/api/users', methods=['GET'])
def api_users():
    if session.get('role') != 'admin':
        return jsonify({"error": "Unauthorized"}), 401
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, role, department, created_at FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
