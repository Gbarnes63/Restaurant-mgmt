from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)
DATABASE = 'restaurant.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn



@app.route('/api/staff/<int:staff_id>', methods=['GET'])
def get_staff_member(staff_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
        staff_member = cursor.fetchone()
        
        conn.close()
        
        if staff_member:
            return jsonify({
                'success': True,
                'data': dict(staff_member)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Staff member not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

      
app.run(host='0.0.0.0', port=5001)