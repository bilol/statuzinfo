from app import app, db

def reset_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Database has been reset and tables created successfully.")

if __name__ == '__main__':
    reset_database()
