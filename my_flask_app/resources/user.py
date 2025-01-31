from flask import request
from flask_restful import Resource
from models import db, User
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
import re

class UserResource(Resource):
    def get(self, user_id=None):
        """Retrieve all users or a specific user by ID."""
        if user_id:
            user = User.query.get(user_id)
            if user:
                return {"id": user.id, "username": user.username, "email": user.email}, 200
            return {"message": "User not found"}, 404

        users = User.query.all()
        return [{"id": user.id, "username": user.username, "email": user.email} for user in users], 200

    def post(self):
        """Create a new user."""
        data = request.get_json()

        # Extract and validate required fields
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return {'message': 'Missing required fields'}, 400

        # Ensure email is formatted correctly (basic check)
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {'message': 'Invalid email format'}, 400

        try:
            # Create new user and use set_password to hash the password
            new_user = User(username=username, email=email)
            new_user.set_password(password)  # Use the set_password method
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User created successfully', 'id': new_user.id}, 201
        except IntegrityError:
            db.session.rollback()
            return {'message': 'Username or email already exists'}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': 'Internal Server Error', 'error': str(e)}, 500

    def put(self, user_id):
        """Update an existing user."""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if username:
            user.username = username
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  # Basic email validation
                return {'message': 'Invalid email format'}, 400
            user.email = email
        if password:  # Only update the password if it's provided
            user.set_password(password)  # Use the set_password method to hash the password

        db.session.commit()
        return {"message": "User updated successfully"}, 200

    def delete(self, user_id):
        """Delete a user."""
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200
