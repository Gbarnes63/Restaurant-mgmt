from flask import Flask, jsonify, request, Response
import sqlite3
from datetime import datetime
import json
from flask_cors import CORS
from Services.AuthService import AuthService 



auth_app = Flask(__name__)
CORS(auth_app, origins=["http://localhost:5173"], supports_credentials=True) 





auth_service = AuthService()

@auth_app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')  

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing username or password'}), 400

    
    login_result = auth_service.validate_login(username, password)

    if login_result['success']:
        token = auth_service.issue_jwt_token(login_result['user_id'], login_result['staff_id'], login_result['username'])
        response = jsonify({'success': True, 'message': 'Login successful'})
        response = auth_service.set_jwt_cookie(response, token)
        return response
    else:
        return jsonify({'success': False, 'error': login_result['error']}), 401

@auth_app.route('/api/verify_jwt', methods=['GET'])
def verify_jwt():
    token = request.cookies.get('jwt_token')
    if not token:
        return jsonify({'success': False, 'error': 'JWT token not found'}), 401

    payload = auth_service.decode_jwt_token(token)
    if payload:
        return jsonify({'success': True, 'user_data': payload})
    else:
        return jsonify({'success': False, 'error': 'Invalid or expired JWT token'}), 401

def start_auth_api():
   
    auth_app.run(host='0.0.0.0', port=5002) # Run on a different port to avoid conflict
