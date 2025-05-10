from flask import Flask, jsonify, request, Response
import sqlite3
from datetime import datetime
import json
from flask_cors import CORS
from functools import wraps
from Services.OrderInputService import OrderInputService
from Classes.Order import Order
from Classes.InventorySystem import InventorySystem
from Services.AuthService import AuthService  # Import the AuthService


# Flask app initialization
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
# Enable CORS for all routes
DATABASE = 'restaurant.db'
JWT_SECRET_KEY = 'your_jwt_secret_key' #Change this to a secure key

# Initialize AuthService
auth_service = AuthService(db_path=DATABASE, jwt_secret=JWT_SECRET_KEY)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            return jsonify({'success': False, 'error': 'Missing JWT token'}), 401
        payload = auth_service.decode_jwt_token(token)
        if not payload:
            return jsonify({'success': False, 'error': 'Invalid or expired JWT token'}), 401
        # Optionally, you can attach the payload to the request context
        # g.user = payload
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/login', methods=['POST'])
def login():
    """
    API endpoint for user login.
    """
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')  # In a real app, this should be the hashed password

        if not username or not password:
            return jsonify({'success': False, 'error': 'Missing username or password'}), 400

        # Validate login using AuthService
        login_result = auth_service.validate_login(username, password)

        if login_result['success']:
            # Issue JWT token
            token = auth_service.issue_jwt_token(login_result['user_id'], login_result['staff_id'], login_result['username'])

            # Set JWT token as an HTTP-only cookie
            response = jsonify({'success': True, 'message': 'Login successful'})
            response = auth_service.set_jwt_cookie(response, token)
            return response, 200
        else:
            return jsonify({'success': False, 'error': login_result['error']}), 401

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@app.route('/api/verify_token', methods=['GET'])
@login_required
def verify_token():
    """
    API endpoint to verify JWT token.
    """
    return jsonify({'success': True, 'message': 'Token is valid'}), 200



@app.route('/api/staff/<int:staff_id>', methods=['GET'])
@login_required
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
@login_required
def get_menu_items():
    try:
        inventory_sys_instance = InventorySystem(1,[])
        menu_items = inventory_sys_instance.getMenuItems()
       
        return jsonify({
            'success': True,
            'data': [dict(item) for item in menu_items]  
        })
    except Exception as e:
         return jsonify({
            'success': False,
            'error': str(e)
        }), 500



@app.route('/api/create_order', methods=['POST'])
@login_required
def create_order():
    try:
        data = request.json  # Get JSON data from frontend

        #Expected format
        # {
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
        order = Order(orderID=1, tableID=table_id, staffID=staff_id, items=menu_items, status="Pending")
       

        # Process order using OrderInputService
        order_service = OrderInputService(order)
        response = order_service.process_order()

        return jsonify(response)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    

@app.route('/api/fetch_order', methods=['GET'])
@login_required
def fetch_order():
    try:
        # Process order using OrderInputService
        order_service = OrderInputService(None)
        response = order_service.get_order(None)

        return jsonify(response)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
