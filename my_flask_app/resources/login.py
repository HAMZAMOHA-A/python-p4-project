from flask_restful import Resource, reqparse
from flask import jsonify
from models import User  # Import User model

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username_or_email', required=True, help="Username or Email is required")
        parser.add_argument('password', required=True, help="Password is required")
        args = parser.parse_args()

        # Find user by username or email
        user = User.query.filter(
            (User.username == args['username_or_email']) | (User.email == args['username_or_email'])
        ).first()

        if user and user.check_password(args['password']):
            user_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
            return jsonify({'message': 'Login successful', 'user': user_data})  # Return properly formatted JSON
        else:
            return jsonify({'message': 'Invalid username/email or password'}), 401  # Make sure response is JSON
