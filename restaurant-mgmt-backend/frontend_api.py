from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import json


from flask_cors import CORS

from Classes.InventorySystem import InventorySystem
from Classes.Order import Order
from Services.OrderInputService import OrderInputService


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
    



@app.route('/api/create_order', methods=['POST'])
def create_order():
    try:
        data = request.json  # Get JSON data from frontend

        #Expected format
#         {
#     "table_number": 3,
#     "staff_id": 1,
#     "menu_items": [
#         {
#             "name": "Margherita Pizza",
#             "itemid": 1,
#             "price": 12.99,
#             "quantity": 2
#         },
#         {
#             "name": "Caesar Salad",
#             "itemid": 2,
#             "price": 8.99,
#             "quantity": 1
#         },
#         {
#             "name": "Chocolate Cake",
#             "itemid": 3,
#             "price": 6.99,
#             "quantity": 3
#         }
#     ]
# }
      
        table_id = data.get("table_number")
        staff_id = data.get("staff_id")
        menu_items = data.get("menu_items", [])

        if not table_id or not staff_id or not menu_items:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Create an Order object
        order = Order(orderID=None, tableID=table_id,staffID=staff_id, items=menu_items, status="Pending")

        # Process order using OrderInputService
        order_service = OrderInputService(order)
        response = order_service.process_order()

        return jsonify(response)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

app.run(host='0.0.0.0', port=5001)