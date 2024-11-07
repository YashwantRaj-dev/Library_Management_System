from config import db, app
from models.user import User, Librarian

def create_librarian():
    username = "lib"
    email = "librarian@example.com"
    password = "libpass"
    role = "librarian"

    # Check if the librarian already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        print("Librarian already exists.")
        return

    # Create the librarian user
    new_user = User(username=username, email=email, password=password, role=role)
    db.session.add(new_user)
    db.session.commit()

    # Create the librarian profile
    librarian = Librarian(user_id=new_user.id)
    db.session.add(librarian)
    db.session.commit()

    print("Librarian created successfully.")

if __name__ == '__main__':
    with app.app_context():
        create_librarian()
