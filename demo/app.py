from flask import Flask, jsonify, request
# from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from werkzeug.security import check_password_hash
from config import app, db
from models.user import User, Librarian, Admin, Section, Book, BookRequest, Review
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
# from task import send_email
from task import send_daily_reminder
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import os 
from flask import send_from_directory

app.config['SECRET_KEY'] = 'voYtbdw2WM1eFKai'

# @app.route('/email')
# def hello_world():
#     send_email.delay("yashwantraj159@gmail.com","rajyashwant0641@gmail.com","Flask","Tertiary")
#     return "email sent"

# Enable CORS
# cors = CORS()
# with app.app_context():
#     cors.init_app(app)

# api = Api(app)

CORS(app, supports_credentials=True)

from flask import g

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'Alert!': 'Token is missing'}), 403
        try:
            token = token.split(" ")[1]  # Bearer token
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user = User.query.filter_by(username=payload['user']).first()
            if not g.user:
                return jsonify({'Alert!': 'User not found'}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({'Alert!': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Alert!': 'Invalid Token!'}), 403
        return func(*args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
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

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    
    if role == 'user':
        existing_user = User.query.filter_by(username=username).first()
    elif role == 'librarian':
        existing_user = User.query.filter_by(username=username).first()
    elif role == 'admin':
        existing_user = User.query.filter_by(username=username).first()
    else:
        return jsonify({"status": "error", "message": "Invalid role"}), 400
    
    if not existing_user or existing_user.password != password:
        return jsonify({"status": "error", "message": "Invalid Credentials"}), 401
    
    existing_user.last_visit = datetime.utcnow()
    db.session.commit()
    
    token = jwt.encode({
        'user': username,
        'role': role,
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return jsonify({'token': token, 'role': role})

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'This is a protected route'})

@app.route('/sections', methods=['GET', 'POST'])
@token_required
def manage_sections():
    if request.method == 'GET':
        sections = Section.query.all()
        if not sections:
            return jsonify({'message': 'No Sections Available'}), 200
        sections_list = [section.to_dict() for section in sections]
        return jsonify(sections_list), 200
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        date_created = datetime.now(timezone.utc)
        
        try:
            new_section = Section.create_section(name, date_created, description)
            return jsonify({'message': 'Section added successfully', 'section': new_section.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/sections/<int:section_id>', methods=['GET', 'DELETE'])
@token_required
def section_detail(section_id):
    if request.method == 'GET':
        section = Section.query.get(section_id)
        if not section:
            return jsonify({'message': 'Section not found'}), 404
        return jsonify({'section': section.to_dict()}), 200
    
    elif request.method == 'DELETE':
        section = Section.query.get(section_id)
        if not section:
            return jsonify({"status": "error", "message": "Section not found"}), 404

        try:
            books = Book.query.filter_by(section_id=section.id).all()
            for book in books:
                db.session.delete(book)

            db.session.delete(section)
            db.session.commit()
            return jsonify({"status": "success", "message": "Section and its books deleted successfully"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/sections/<int:section_id>/books', methods=['GET', 'POST'])
@cross_origin()
@token_required
def books_in_section(section_id):
    if request.method == 'GET':
        try:
            books = Book.query.filter_by(section_id=section_id).all()
            return jsonify({'books': [book.to_dict() for book in books]})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    elif request.method == 'POST':
        if not g.user or g.user.role != 'librarian':
            return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        content = data.get('content')
        
        if not title or not author or not content:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        try:
            new_book = Book.create_book(title, author, content, section_id, g.user.id)
            return jsonify({'book': new_book.to_dict()}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400
        
@app.route('/requests', methods=['GET'])
@token_required
def get_requests():
    try:
        requests = BookRequest.query.filter(BookRequest.status == 'pending').all()
        return jsonify({'requests': [request.to_dict() for request in requests]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/requests/<int:request_id>/<string:action>', methods=['POST'])
@token_required
def handle_request(request_id, action):
    try:
        request = BookRequest.query.get(request_id)
        if not request or request.status == 'cancelled':
            return jsonify({'status': 'error', 'message': 'Request not found'}), 404

        if action == 'grant':
            request.status = 'granted'
            request.date_granted = datetime.utcnow()
            request.return_date = request.date_granted + timedelta(days=request.days_requested)
            db.session.commit()
            return jsonify({'message': f'Access granted to {request.user.username}', 'request': request.__repr__()}), 200

        elif action == 'reject':
            request.status = 'rejected'
            db.session.commit()
            return jsonify({'message': 'Request rejected', 'request': request.__repr__()}), 200

        return jsonify({'status': 'error', 'message': 'Invalid action'}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/sections/<int:section_id>', methods=['PUT'])
@cross_origin()
@token_required
def modify_section(section_id):
    if not g.user or g.user.role != 'librarian':
        return jsonify({"status": "error", "message": "Unauthorized"}), 403
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    
    if not name or not description:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400
    
    section = Section.query.get(section_id)
    if not section:
        return jsonify({"status": "error", "message": "Section not found"}), 404
    
    try:
        section.name = name
        section.description = description
        db.session.commit()
        return jsonify({'message': 'Section Modified Successfully', 'section': section.to_dict()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
@token_required
def handle_book(book_id):
    if request.method == 'GET':
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        return jsonify({'book': book.to_dict()}), 200

    elif request.method == 'PUT':
        if not g.user or g.user.role != 'librarian':
            return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
        data = request.get_json()
        title = data.get('title')
        author = data.get('author')
        content = data.get('content')
        
        if not title or not author or not content:
            return jsonify({"status": "error", "message": "Missing required fields"}), 400
        
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        
        try:
            book.title = title
            book.author = author
            book.content = content
            db.session.commit()
            return jsonify({'message': 'Book Modified Successfully', 'book': book.to_dict()}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    elif request.method == 'DELETE':
        if not g.user or g.user.role != 'librarian':
            return jsonify({"status": "error", "message": "Unauthorized"}), 403
        
        book = Book.query.get(book_id)
        if not book:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        
        try:
            db.session.delete(book)
            db.session.commit()
            return jsonify({'message': 'Book Deleted Successfully'}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/books', methods=['GET'])
@cross_origin()
def get_books():
    try:
        books = Book.query.all()
        print(books)
        return jsonify({'books': [book.to_dict() for book in books]}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/books/<int:book_id>/request', methods=['POST'])
@cross_origin()
def request_book(book_id):
    username = request.json.get('username')
    days_requested = request.json.get('days_requested')
    print("request",book_id)
    print(username)  
    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400

    user = User.query.filter_by(username=username).first()
    print(user) 
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id
    try:
        existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id, status='pending').first()
        if existing_request:
            return jsonify({"status": "error", "message": "Request already pending"}), 400

        new_request = BookRequest.create_request(user_id, book_id, days_requested)
        return jsonify({'message': 'Request sent to Librarian', 'request': new_request.id}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/books/<int:book_id>/cancel_request', methods=['POST'])
@cross_origin()
def cancel_request(book_id):
    username = request.json.get('username')

    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id
    try:
        existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id, status='pending').first()
        if not existing_request:
            return jsonify({"status": "error", "message": "No pending request found"}), 400

        existing_request.status = 'cancelled'
        db.session.commit()
        return jsonify({'message': 'Request cancelled successfully'}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/books/<int:book_id>/return', methods=['POST'])
@cross_origin()
def return_book(book_id):
    username = request.json.get('username')

    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id
    try:
        existing_request = BookRequest.query.filter_by(user_id=user_id, book_id=book_id, status='granted').first()
        if not existing_request:
            return jsonify({"status": "error", "message": "No granted request found for this book"}), 400

        existing_request.status = 'returned'
        db.session.commit()
        return jsonify({'message': 'Book returned successfully'}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/users/books', methods=['GET'])
@cross_origin()
def get_user_books():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400
     
    user = User.query.filter_by(username=username).first()
      
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id
    
    try:
        granted_books = BookRequest.query.filter_by(user_id=user_id, status='granted').all()
        pending_books = BookRequest.query.filter_by(user_id=user_id, status='pending').all()
        
        books_to_be_completed = [book.to_dict() for book in granted_books if not book.is_completed or book.is_completed in [False, None, 0]]
        books_completed = [book.to_dict() for book in granted_books if book.is_completed or book.is_completed in [True, 1]]
        books_pending = [book.to_dict() for book in pending_books]
        
        books_to_be_completed = [
            {
                'id': book['id'],               #Book Request Id
                'book_id': book['book_id'],
                'title': book['book_title'],
                'author': book['book_author'],
                'section': book['book_section']
            } for book in books_to_be_completed
        ]
        books_completed = [
            {
                'id': book['id'],               #Book Request Id
                'book_id': book['book_id'],
                'title': book['book_title'],
                'author': book['book_author'],
                'section': book['book_section']
            } for book in books_completed
        ]
        books_pending = [
            {
                'id': book['id'],
                'book_id': book['book_id'],
                'title': book['book_title'],
                'author': book['book_author'],
                'section': book['book_section']
            } for book in books_pending
        ]
    
        return jsonify({
            'booksToBeCompleted': books_to_be_completed,
            'booksCompleted': books_completed,
            'booksPending': books_pending
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500



@app.route('/books/<int:book_id>/feedback', methods=['POST'])
@cross_origin()
@token_required
def submit_feedback(book_id):
    username = request.json.get('username')
    rating = request.json.get('rating')
    review = request.json.get('review')

    if not username or rating is None:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    try:
        new_review = Review.create_review(user.id, book_id, rating, review)
        
        # Update the book's average rating
        book = Book.query.filter_by(id=book_id).first()
        if book:
            all_reviews = Review.query.filter_by(book_id=book_id).all()
            total_ratings = sum(review.rating for review in all_reviews)
            avg_rating = total_ratings / (len(all_reviews))
            book.rating = avg_rating
            db.session.commit()

        return jsonify({'message': 'Feedback submitted successfully', 'review': new_review.to_dict()}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/books/<int:book_id>/complete', methods=['POST'])
@cross_origin()
def mark_book_complete(book_id):
    username = request.json.get('username')

    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    book_request = BookRequest.query.filter_by(user_id=user.id, book_id=book_id, status='granted').first()
    if not book_request:
        return jsonify({"status": "error", "message": "No granted book found for this user"}), 404

    try:
        book_request.is_completed = True
        db.session.commit()
        return jsonify({"status": "success", "message": "Book marked as complete"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/userreadbooks/<int:book_id>', methods=['GET'])
@cross_origin()
def get_book(book_id):
    try:
        # Fetch the book from the database using the book_id
        print(book_id) 
        book = Book.query.filter_by(id=book_id).first()
        
        print(book) 
        # If the book is not found, return a 404 error
        if not book:
            return jsonify({"status": "error", "message": "Book not found"}), 404
        
        # Return the book details in JSON format
        return jsonify({'book': book.to_dict()}), 200
    except Exception as e:
        # Log the error and return a 500 status
        print(f"Error occurred: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to get user stats

@app.route('/user/stats', methods=['GET'])
@cross_origin()
def get_user_stats():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id

    try:
        books_completed = BookRequest.query.filter_by(user_id=user_id, is_completed=True).count()
        books_reviewed = Review.query.filter_by(user_id=user_id).count()
        
        stats = {
            'booksCompleted': books_completed,
            'booksReviewed': books_reviewed
        }

        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Route to generate section bar chart

@app.route('/user/section_barchart', methods=['GET'])
@cross_origin()
def get_section_barchart():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id

    try:
        query = db.session.query(Section.name.label('section_name'),func.count(BookRequest.id).label('request_count'))
        print("Query base:", query)
        
        query = query.join(Book, Book.id == BookRequest.book_id)\
                     .join(Section, Book.section_id == Section.id)
        print("After join:", query)
        
        # Before applying the filter
        total_requests = BookRequest.query.filter_by(user_id=user_id).count()
        print(f"Total requests for user {user_id}: {total_requests}")
        
        query = query.filter(BookRequest.user_id == user_id, BookRequest.is_completed == True)
        print("After filter:", query)
        
        query = query.group_by(Section.id)
        print("After group by:", query)
        
        sections = query.all()
        print(sections) 

        section_names = [section[0] for section in sections]
        section_counts = [section[1] for section in sections]
        
        print("sn",section_names)
        print("sc",section_counts)     
        
        # plt.figure(figsize=(10, 5))
        # sns.barplot(x=section_names, y=section_counts)
        # plt.xlabel('Section')
        # plt.ylabel('Number of Books Read')
        # plt.title('Books Read in Different Sections')

        # img = io.BytesIO()
        # plt.savefig(img, format='png')
        # img.seek(0)
        # plot_url = base64.b64encode(img.getvalue()).decode()

        # plt.close()
        
        df = pd.DataFrame(sections, columns=['section_name', 'request_count'])
        
        # Check if DataFrame is empty
        if df.empty:
            return jsonify({"status": "error", "message": "No data found for the given user."}), 404

        fig = go.Figure(data=[
            go.Bar(
                x=df['section_name'],  # X-axis data (section names)
                y=df['request_count'],  # Y-axis data (counts)
                marker_color='indigo'  # Customize the bar color
            )
        ])
        unique_counts = sorted(set(df['request_count'].astype(int)))
        # Update layout for the chart
        fig.update_layout(
            title='Books Read in Different Sections',
            xaxis_title='Section',
            yaxis_title='Number of Books Read',
            template='plotly_white',  # Optional: use a template
            yaxis_tickvals=unique_counts
        )

        # Save the figure to a BytesIO object
        # img = io.BytesIO()
        # fig.write_image(img, format='png')  # Save as PNG image
        # img.seek(0)
        # plot_url = base64.b64encode(img.getvalue()).decode()  # Encode to base64
        # print(plot_url) 
        
        # return jsonify({'plot_url': f'data:image/png;base64,{plot_url}'}), 200
        
        charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')

        # Create the directory if it doesn't exist
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)

        # # Save the figure as a PNG file in the charts directory
        try:
            fig.write_image(os.path.join(charts_dir, 'barchart.png'))
            print("Image successfully saved")
        except Exception as e:
            print(f"Error saving image: {str(e)}")

        # Optionally, you can also return the plot_html if needed
        plot_html = fig.to_html(full_html=False)
        # print(plot_html) 
        return jsonify({'plot_html': plot_html}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/user/barchart_image', methods=['GET'])
@cross_origin()
def get_barchart_image():
    # Verify JWT token (implement your own token verification)
 
    # Serve the barchart.png from the charts directory
    return send_from_directory('charts', 'barchart.png')


# Route to generate section pie chart

@app.route('/user/section_piechart', methods=['GET'])
@cross_origin()
def get_section_piechart():
    username = request.args.get('username')
    
    if not username:
        return jsonify({"status": "error", "message": "Username is missing"}), 400
    
    user = User.query.filter_by(username=username).first()
    print(user) 
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    user_id = user.id
    print(user_id)
    try:
        # sections = db.session.query(Book.section_name, db.func.count(BookRequest.id)).\
        #            join(BookRequest, Book.id == BookRequest.book_id).\
        #            filter(BookRequest.user_id == user_id, BookRequest.is_completed == True).\
        #            group_by(Book.section_name).all()
        
        print("Try") 
        query = db.session.query(Section.name.label('section_name'),func.count(BookRequest.id).label('request_count'))
        print("Query base:", query)
        
        query = query.join(Book, Book.id == BookRequest.book_id)\
                     .join(Section, Book.section_id == Section.id)
        print("After join:", query)
        
        # Before applying the filter
        total_requests = BookRequest.query.filter_by(user_id=user_id).count()
        print(f"Total requests for user {user_id}: {total_requests}")
        
        query = query.filter(BookRequest.user_id == user_id, BookRequest.is_completed == True)
        print("After filter:", query)
        
        query = query.group_by(Section.id)
        print("After group by:", query)
        
        sections = query.all()
        print(sections) 

        section_names = [section[0] for section in sections]
        section_counts = [section[1] for section in sections]
        
        print("sn",section_names)
        print("sc",section_counts)     
        
        # plt.figure(figsize=(8, 8))
        # plt.pie(section_counts, labels=section_names, autopct='%1.1f%%', startangle=140)
        # plt.title('Section Distribution of Books Read')

        # img = io.BytesIO()
        # plt.savefig(img, format='png')
        # img.seek(0)
        # plot_url = base64.b64encode(img.getvalue()).decode()

        # plt.close()
        
        df = pd.DataFrame(sections, columns=['section_name', 'request_count'])
        
        # Check if DataFrame is empty
        if df.empty:
            return jsonify({"status": "error", "message": "No data found for the given user."}), 404

        # Plotting the pie chart using pandas
        fig = px.pie(df, names='section_name', values='request_count', title='Section Distribution of Books Read')

        # Save the plot to a BytesIO object
        # img = io.BytesIO()
        # img.seek(0)
        # plot_url = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Generate HTML string

        charts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'charts')
        
        if not os.path.exists(charts_dir):
            os.makedirs(charts_dir)

        # Save the figure as a PNG image
        fig.write_image(os.path.join(charts_dir, 'piechart.png'))

        # plt.close()
        plot_html = fig.to_html(full_html=False)
        # print(plot_url) 
        # return jsonify({'plot_url': f'data:image/png;base64,{plot_url}'}), 200
        return jsonify({'plot_url': plot_html}), 200
    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print the error
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/user/piechart_image', methods=['GET'])
@cross_origin()
def get_piechart_image():
    # Verify JWT token (implement your own token verification)
    
    # Serve the piechart.png from the charts directory
    return send_from_directory('charts', 'piechart.png')

@app.route('/librarian/piechart_image', methods=['GET'])
@cross_origin()
def get_librarian_piechart_image():
    return send_from_directory('charts', 'libpiechart.png')


@app.route('/books/<int:book_id>/reviews', methods=['GET'])
@cross_origin()
@token_required
def get_book_reviews(book_id):
    reviews = Review.query.filter_by(book_id=book_id).all()
    return jsonify([review.to_dict() for review in reviews])

@app.route('/update_book_requests', methods=['PUT'])
@cross_origin()
@token_required
def update_book_requests():
    # This will be executed when the user dashboard is opened
    try:
        # Get all book requests
        requests = BookRequest.query.all()
        
        for req in requests:
            if req.return_date and req.return_date < datetime.utcnow():
                req.status = 'returned'  # Change the status to returned
                req.is_completed = True  # Mark as completed if needed
                db.session.commit()  # Commit the changes

        return jsonify({'message': 'Book requests updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/librarian/stats', methods=['GET'])
@cross_origin()
def librarian_stats():
    try:
        sections = Section.query.all()
        section_data = []
        
        for section in sections:
            book_count = Book.query.filter_by(section_id=section.id).count()  # Count books in each section
            section_data.append((section.name, book_count))
        
        df = pd.DataFrame(section_data, columns=['section_name', 'book_count'])
        
        # Check if DataFrame is empty
        if df.empty:
            return jsonify({"status": "error", "message": "No sections found."}), 404
        
        fig = px.pie(df, names='section_name', values='book_count', title='Section Wise Distribution of Books')
        
        # Save the pie chart as HTML
        plot_url = fig.to_html(full_html=False, include_plotlyjs='cdn')
        
        # Save the pie chart image to the charts directory
        img_path = 'charts/libpiechart.png'  # Adjust path as necessary
        fig.write_image(img_path)
        
        return jsonify({'plot_html': plot_url}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/librarian/data', methods=['GET'])
@cross_origin()
def librarian_data():
    # Total number of unique users
    total_users = User.query.count()
    
    # Total number of books
    total_books = Book.query.count()

    # Get granted requests
    granted_requests = BookRequest.query.filter_by(status='granted').all()

    # Prepare a list of users and their granted books
    user_books = {}
    for request in granted_requests:
        username = request.user.username
        book_title = request.book.title
        
        if username not in user_books:
            user_books[username] = []
        user_books[username].append(book_title)

    return jsonify({
        'total_users': total_users,
        'total_books': total_books,
        'user_books': user_books
    })


# api.add_resource(Register, '/register')
# api.add_resource(Login, '/login')
# api.add_resource(Protected, '/protected')
# api.add_resource(SectionResource, '/sections', '/sections/<int:section_id>') 
# api.add_resource(BookResource, '/books', '/sections/<int:section_id>/books')
# api.add_resource(RequestResource, '/requests', '/requests/<int:request_id>/<string:action>')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
