# Define your models

from config import db
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    last_visit = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return '<User %r>' % self.username

    @classmethod
    def return_users(cls):
        return cls.query.all()

    @classmethod
    def create_user(cls, username, email, password, role='user'):
        new_user = cls(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @classmethod
    def get_user_by_uname(cls, uname):
        return cls.query.filter_by(username=uname).first()


class Librarian(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('librarian', uselist=False, lazy=True))

    def __repr__(self):
        return '<Librarian %r>' % self.id

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('admin', uselist=False, lazy=True))

    def __repr__(self):
        return '<Admin %r>' % self.id
    
class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Section %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_created': self.date_created.isoformat(),
            'description': self.description
        }
        
    @classmethod
    def create_section(cls, name, date_created, description=None):
        new_section = cls(name=name, date_created=date_created, description=description)
        db.session.add(new_section)
        db.session.commit()
        return new_section

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', backref=db.backref('books', lazy=True))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploader = db.relationship('User', backref=db.backref('uploaded_books', lazy=True))
    rating = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return '<Book %r>' % self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'section_name': self.section.name,
            'section_id': self.section_id,
            'uploaded_by': self.uploaded_by,
            'rating': self.rating
        }
    
    @classmethod
    def create_book(cls, title, author, content, section_id, uploaded_by):
        new_book = cls(title=title, author=author, content=content, section_id=section_id, uploaded_by=uploaded_by,rating=5)
        db.session.add(new_book)
        db.session.commit()
        return new_book

class BookRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('requests', lazy=True))
    days_requested = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='pending')
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_granted = db.Column(db.DateTime, nullable=True)
    return_date = db.Column(db.DateTime, nullable=True)
    access_granted_at = db.Column(db.DateTime, nullable=True)
    rating = db.Column(db.Float, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return '<BookRequest %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'book_author': self.book.author,
            'book_section': self.book.section.name,
            'days_requested': self.days_requested,
            'status': self.status,
            'date_requested': self.date_requested,
            'date_granted': self.date_granted,
            'return_date': self.return_date,
            'access_granted_at': self.access_granted_at,
            'is_completed': self.is_completed
        }
    
    @classmethod
    def create_request(cls, user_id, book_id, days_requested):
        new_request = cls(user_id=user_id, book_id=book_id, days_requested=days_requested, date_requested=datetime.utcnow())
        db.session.add(new_request)
        db.session.commit()
        return new_request

    @classmethod
    def grant_access(cls, request_id):
        request = cls.query.get(request_id)
        request.status = 'granted'
        request.access_granted_at = datetime.utcnow()
        request.return_date = request.access_granted_at + timedelta(days=request.days_requested)
        db.session.commit()
        return request

    @classmethod
    def revoke_access(cls, request_id):
        request = cls.query.get(request_id)
        request.status = 'revoked'
        db.session.commit()
        return request

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('reviews', lazy=True))
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<Review %r>' % self.id

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username,
            'book_id': self.book_id,
            'book_title': self.book.title,
            'rating': self.rating,
            'comment': self.comment
        }
    
    @classmethod
    def create_review(cls, user_id, book_id, rating, comment=None):
        new_review = cls(user_id=user_id, book_id=book_id, rating=rating, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        return new_review

