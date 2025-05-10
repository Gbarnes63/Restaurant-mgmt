import sqlite3
import jwt
from datetime import datetime, timedelta
from http.cookies import SimpleCookie
from DbHandler import DatabaseHandler

class AuthService:
    def __init__(self, db_path='./DB/OrdersDB.db'): 
        
        self.db_path = "./DB/LoginsDB.db"
        self.jwt_secret = "Testing"
        self.jwt_algorithm = "HS256" 
        self.db= DatabaseHandler(self.db_path) 
        



    def validate_login(self, username, password):
        """
        Validates user login credentials against the database.
        """
        db_handler = DatabaseHandler(self.db_path)  # Create a new instance
        try:
            print(f'received username and password {username} and password {password}')

            user_data = db_handler.fetch_one(
                """
                SELECT
                    id,
                    staff_id,
                    username,
                    last_login,
                    is_active
                FROM
                    staff_login
                WHERE
                    username = ?
                    AND password_hash = ?
                    AND is_active = 1;
                """,
                (username, password)
            )

            print (list(user_data))
            if user_data:
                user_id, staff_id, username, last_login, is_active = user_data
                db_handler.perform_query("UPDATE staff_login SET last_login = CURRENT_TIMESTAMP WHERE id = ?", (user_id,))
                return {"success": True, "user_id": user_id, "staff_id": staff_id, "username": username}
            else:
                return {"success": False, "error": "Invalid credentials"}
        except sqlite3.Error as e:
            return {"success": False, "error": str(e)}
        finally:
            db_handler.close_connection() 
      

    def issue_jwt_token(self, user_id, staff_id, username): 
       
        payload = {
            'user_id': user_id,
            'staff_id': staff_id,
            'username': username, 
            'exp': datetime.utcnow() + timedelta(hours=1)  
        }
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        return token

    def set_jwt_cookie(self, response, token):
        
        cookie = SimpleCookie()
        cookie['jwt_token'] = token
        cookie['jwt_token']['httponly'] = True
        cookie['jwt_token']['path'] = '/'  
        response.headers['Set-Cookie'] = cookie.output(header='')
        return response # Return the response
    
    def decode_jwt_token(self, token):
        
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid Token")
            return None
        

