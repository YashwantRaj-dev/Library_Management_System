from config import db, app
from models.user import User

def update_user_email(old_email, new_email):
    # Fetch the librarian user by the old email
    user = User.query.filter_by(email=old_email).first()
    
    if user:
        # Update the email
        user.email = new_email
        db.session.commit()
        print("User's email updated successfully.")
    else:
        print("User not found.")

if __name__ == '__main__':
    with app.app_context():
        update_user_email("abc@email.com", "yashwantarcade01@gmail.com")
