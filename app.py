from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

@app.route("/")
def home():
    return "Secure File Sharing Platform is running!"

if __name__ == "__main__":
    app.run(debug=True)