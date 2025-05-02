from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json


from flask_cors import CORS

from Classes.InventorySystem import InventorySystem


# Flask app initialization
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
# Enable CORS for all routes
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
    

@app.route('/api/menu-items', methods=['GET'])
def get_menu_items():
   
  
        
        inventory_sys_instance = InventorySystem(1,[])

        menu_items = inventory_sys_instance.getMenuItems()
        print(menu_items)
       
        return jsonify({
            'success': True,
            'data': [dict(item) for item in menu_items]  
        })
    



@app.route('/api/create order', methods=['POST'])
def create_order():
    try:
        
        conn = get_db_connection()
        cursor = conn.cursor()
       
        cursor.execute("SELECT * FROM menu_items")#change to insert query
        
       
        conn.close()
       
        return jsonify({
            'success': True,
            'data': 'db response'
        })
    except Exception as e:
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


app.run(host='0.0.0.0', port=5001)