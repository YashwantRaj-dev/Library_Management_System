from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from config import app, db
from models.user import User, Librarian, Admin, Section, Book, BookRequest

app.config['SECRET_KEY'] = 'voYtbdw2WM1eFKai'

# Enable CORS
# CORS(app)
# cors = CORS()
# CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow access to all origins for all /api/* routes
api = Api(app)

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 403
        try:
            token = token.split(" ")[1]  # Bearer token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 403
        return func(*args, **kwargs)
    return decorated

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
                
        if password != confirm_password:
            return {"status": "error", "message": "Passwords do not match"}, 400
        
        try:
            User.create_user(username, email, password)
            return {"status": "success", "message": f"User created successfully: {username}"}, 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        
        if role == 'user':
            existing_user = User.get_user_by_uname(username)
        elif role == 'librarian':
            existing_user = Librarian.query.join(User).filter(User.username == username).first()
        elif role == 'admin':
            existing_user = Admin.query.join(User).filter(User.username == username).first()
        else:
            return jsonify({"status": "error", "message": "Invalid role"}), 400
        
        if not existing_user or existing_user.user.password != password:
            return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
        
        token = jwt.encode({
            'user': username,
            'role': role,
            'exp': datetime.now(timezone.utc) + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({'token': token, 'role': role})

class Protected(Resource):
    @token_required
    def get(self):
        return jsonify({'message': 'This is a protected route'})

class SectionResource(Resource):
    @token_required
    def get(self):
        try:
            # sections = Section.query.all()
            # return jsonify({'sections': [section.__repr__() for section in sections]})
            return "Hello"
        except Exception as e:
            print("Error fetching sections: ", e)  # Debug log
            return {"status": "error", "message": str(e)}, 500

    @token_required
    def post(self):
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        date_created = datetime.now(timezone.utc)

        try:
            new_section = Section.create_section(name, date_created, description)
            return jsonify({'section': new_section.__repr__()}), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

class BookResource(Resource):
    @token_required
    def get(self, section_id):
        books = Book.query.filter_by(section_id=section_id).all()
        return jsonify({'books': [book.__repr__() for book in books]})

    @token_required
    def post(self):
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        content = data.get('content')
        section_id = data.get('section_id')
        uploaded_by = request.user.id

        try:
            new_book = Book.create_book(title, author, content, section_id, uploaded_by)
            return jsonify({'book': new_book.__repr__()}), 201
        except Exception as e:
            return {"status": "error", "message": str(e)}, 400

class RequestResource(Resource):
    @token_required
    def get(self):
        requests = BookRequest.query.all()
        return jsonify({'requests': [request.__repr__() for request in requests]})

    @token_required
    def post(self, request_id, action):
        if action == 'grant':
            request = BookRequest.grant_access(request_id)
        elif action == 'reject':
            request = BookRequest.revoke_access(request_id)
        return jsonify({'request': request.__repr__()})

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Protected, '/api/protected')
api.add_resource(SectionResource, '/api/sections') #'/api/sections/<int:section_id>'
api.add_resource(BookResource, '/api/books', '/api/sections/<int:section_id>/books')
api.add_resource(RequestResource, '/api/requests', '/api/requests/<int:request_id>/<string:action>')

if __name__ == '__main__':
    app.run(debug=True)
