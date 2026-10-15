
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todos.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)

    priority = db.Column(db.String(20), nullable=False)
    due_date = db.Column(db.Date, nullable=True)

    # True means the task is active.
    # False means the task is completed.
    active = db.Column(db.Boolean, default=True, nullable=False)

    # Soft-delete field
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)



@app.route("/")
def index():
    todos = Todo.query.filter_by(is_deleted=False).order_by(
        Todo.due_date.asc(), Todo.id.desc()
    ).all()

    active_todos = [todo for todo in todos if todo.active]
    completed_todos = [todo for todo in todos if not todo.active]

    return render_template(
        "index.html",
        active_todos=active_todos,
        completed_todos=completed_todos
    )


@app.route("/add", methods=["GET", "POST"])
def add_todo():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        due_date_text = request.form.get("due_date", "")

        if not title:
            return render_template(
                "add.html",
                error="Title is required.",
                title=title,
                description=description,
                priority=priority,
                due_date=due_date_text
            )

        if priority not in ["Low", "Medium", "High"]:
            priority = "Medium"

        due_date = None

        if due_date_text:
            try:
                due_date = datetime.strptime(
                    due_date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                return render_template(
                    "add.html",
                    error="Please enter a valid due date.",
                    title=title,
                    description=description,
                    priority=priority,
                    due_date=due_date_text
                )

        todo = Todo(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            active=True,
            is_deleted=False
        )

        db.session.add(todo)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
def edit_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None or todo.is_deleted:
        abort(404)

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        priority = request.form.get("priority", "Medium")
        due_date_text = request.form.get("due_date", "")

        if not title:
            return render_template(
                "edit.html",
                todo=todo,
                error="Title is required."
            )

        if priority not in ["Low", "Medium", "High"]:
            priority = "Medium"

        due_date = None

        if due_date_text:
            try:
                due_date = datetime.strptime(
                    due_date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                return render_template(
                    "edit.html",
                    todo=todo,
                    error="Please enter a valid due date."
                )

        todo.title = title
        todo.description = description
        todo.priority = priority
        todo.due_date = due_date

        db.session.commit()

        return redirect(url_for("index"))

    return render_template("edit.html", todo=todo)


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None or todo.is_deleted:
        abort(404)

    todo.active = not todo.active
    db.session.commit()

    return redirect(url_for("index"))


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete_todo(todo_id):
    todo = db.session.get(Todo, todo_id)

    if todo is None or todo.is_deleted:
        abort(404)

    # Do not delete the database record.
    todo.is_deleted = True
    db.session.commit()

    return redirect(url_for("index"))


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
