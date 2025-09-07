from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Capsule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # motivation, friendship, etc.
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    trigger_date = db.Column(db.DateTime)  # when capsule should be unlocked
