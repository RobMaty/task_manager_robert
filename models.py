from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

STATUS_CHOICES = ["Backlog", "In Progress", "QA", "Done"]

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="Backlog")

    def __repr__(self):
        return f"<Task {self.title} - {self.status}>"
