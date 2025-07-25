from flask import Flask, render_template, request, redirect, url_for
from models import db, Task, STATUS_CHOICES
from flask import jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Main route for index.html
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        if title:
            new_task = Task(title=title, description=description)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for("index"))

    tasks_by_status = {
        status: Task.query.filter_by(status=status).all()
        for status in STATUS_CHOICES
    }
    return render_template("index.html", tasks_by_status=tasks_by_status)

# Route update status
@app.route("/update_status/<int:task_id>", methods=["POST"])
def update_status(task_id):
    data = request.get_json()
    new_status = data.get("status")
    if new_status in STATUS_CHOICES:
        task = Task.query.get_or_404(task_id)
        task.status = new_status
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "error": "Invalid status"}), 400

# Route delete task
@app.route("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

# Route edit task
@app.route("/edit_task", methods=["POST"])
def edit_task():
    task_id = request.form.get("task_id")
    title = request.form.get("title")
    description = request.form.get("description")

    task = Task.query.get_or_404(task_id)
    task.title = title
    task.description = description
    db.session.commit()

    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=False)
