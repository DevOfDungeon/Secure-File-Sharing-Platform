from app import app, db
import models  # registers the models with db

with app.app_context():
    db.create_all()
    print("Tables created.")