import math
from datetime import date
from urllib.parse import quote
from fastapi import FastAPI, Request, Response, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import Base, engine, get_db
from models import User, Task
from auth import (
    hash_password,
    verify_password,
    set_auth_cookies,
    clear_auth_cookies,
    get_current_user,
    decode_token
)

app = FastAPI(title="Todo App")

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

PAGE_SIZE = 10


def redirect_page(url, message=""):
    if message:
        separator = "&" if "?" in url else "?"
        url += separator + "message=" + quote(message)

    return RedirectResponse(url=url, status_code=303)


def get_page_user(request, response, db):
    try:
        return get_current_user(request, response, db)
    except HTTPException:
        return None


def get_task_for_user(task_id, user_id, db):
    return db.query(Task).filter(
        Task.id == task_id,
        Task.createdby == user_id
    ).first()


def get_task_query(db, user, search, status, priority):
    query = db.query(Task).filter(Task.createdby == user.id)

    if search.strip():
        query = query.filter(Task.title.contains(search.strip()))

    if status == "completed":
        query = query.filter(Task.iscompleted.is_(True))
    elif status == "pending":
        query = query.filter(Task.iscompleted.is_(False))
    else:
        status = "all"

    if priority in ["Low", "Medium", "High"]:
        query = query.filter(Task.priority == priority)
    else:
        priority = "all"

    return query, status, priority


@app.get("/")
def home(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if user:
        return RedirectResponse("/dashboard", status_code=303)

    return RedirectResponse("/login", status_code=303)


@app.get("/login")
def login_page(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if user:
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"message": request.query_params.get("message", "")},
        headers={"Cache-Control": "no-store"}
    )


@app.get("/register")
def register_page(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if user:
        return RedirectResponse("/dashboard", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={"message": request.query_params.get("message", "")},
        headers={"Cache-Control": "no-store"}
    )


@app.post("/register")
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    username = username.strip()
    email = email.strip().lower()

    if len(username) < 3 or len(username) > 50:
        return redirect_page("/register", "Username must be between 3 and 50 characters")

    if len(email) > 255 or "@" not in email:
        return redirect_page("/register", "Enter a valid email address")

    if len(password) < 8 or len(password) > 72:
        return redirect_page("/register", "Password must be between 8 and 72 characters")

    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return redirect_page("/register", "Username or email already exists")

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return redirect_page("/register", "Username or email already exists")

    return redirect_page("/login", "Account created successfully. Please log in.")


@app.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == username.strip()
    ).first()

    if not user or not verify_password(password, user.hashed_password):
        return redirect_page("/login", "Incorrect username or password")

    response = RedirectResponse("/dashboard", status_code=303)
    set_auth_cookies(response, user.id)
    response.headers["Cache-Control"] = "no-store"

    return response


@app.get("/dashboard")
def dashboard(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    latest_tasks = db.query(Task).filter(
        Task.createdby == user.id
    ).order_by(Task.id.desc()).limit(2).all()

    all_tasks = db.query(Task).filter(
        Task.createdby == user.id
    ).all()

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "latest_tasks": latest_tasks,
            "total_count": len(all_tasks),
            "completed_count": sum(1 for task in all_tasks if task.iscompleted),
            "pending_count": sum(1 for task in all_tasks if not task.iscompleted),
            "message": request.query_params.get("message", "")
        },
        headers={"Cache-Control": "no-store"}
    )


@app.get("/tasks")
def tasks_page(
    request: Request,
    response: Response,
    page: int = 1,
    search: str = "",
    status: str = "all",
    priority: str = "all",
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    page = max(1, page)

    query, status, priority = get_task_query(
        db, user, search, status, priority
    )

    total_matching_tasks = query.count()
    total_pages = max(1, math.ceil(total_matching_tasks / PAGE_SIZE))
    page = min(page, total_pages)

    tasks = query.order_by(Task.id.desc()).offset(
        (page - 1) * PAGE_SIZE
    ).limit(PAGE_SIZE).all()

    return templates.TemplateResponse(
        request=request,
        name="tasks.html",
        context={
            "user": user,
            "tasks": tasks,
            "search": search,
            "status": status,
            "priority": priority,
            "page": page,
            "total_pages": total_pages,
            "total_matching_tasks": total_matching_tasks,
            "start_task": (page - 1) * PAGE_SIZE + 1 if total_matching_tasks else 0,
            "end_task": min(page * PAGE_SIZE, total_matching_tasks),
            "message": request.query_params.get("message", "")
        },
        headers={"Cache-Control": "no-store"}
    )


@app.post("/tasks/create")
def create_task(
    request: Request,
    response: Response,
    title: str = Form(...),
    description: str = Form(""),
    date_value: str = Form("", alias="date"),
    priority: str = Form("Medium"),
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    title = title.strip()

    if not title or len(title) > 200:
        return redirect_page("/dashboard", "Task title must be between 1 and 200 characters")

    if priority not in ["Low", "Medium", "High"]:
        return redirect_page("/dashboard", "Invalid priority")

    try:
        task_date = date.fromisoformat(date_value) if date_value else None
    except ValueError:
        return redirect_page("/dashboard", "Invalid task date")

    task = Task(
        title=title,
        description=description.strip() or None,
        date=task_date,
        priority=priority,
        iscompleted=False,
        createdby=user.id
    )

    db.add(task)
    db.commit()

    return redirect_page("/dashboard", "Task created successfully")


@app.post("/tasks/{task_id}/edit")
def edit_task(
    task_id: int,
    request: Request,
    response: Response,
    title: str = Form(...),
    description: str = Form(""),
    date_value: str = Form("", alias="date"),
    priority: str = Form("Medium"),
    iscompleted: str = Form("false"),
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    task = get_task_for_user(task_id, user.id, db)

    if not task:
        return redirect_page("/tasks", "Task not found")

    title = title.strip()

    if not title or len(title) > 200:
        return redirect_page("/tasks", "Invalid task title")

    if priority not in ["Low", "Medium", "High"]:
        return redirect_page("/tasks", "Invalid priority")

    if iscompleted not in ["true", "false"]:
        return redirect_page("/tasks", "Invalid task status")

    try:
        task_date = date.fromisoformat(date_value) if date_value else None
    except ValueError:
        return redirect_page("/tasks", "Invalid task date")

    task.title = title
    task.description = description.strip() or None
    task.date = task_date
    task.priority = priority
    task.iscompleted = iscompleted == "true"

    db.commit()

    return redirect_page("/tasks", "Task updated successfully")


@app.post("/tasks/{task_id}/complete")
def complete_task(
    task_id: int,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    task = get_task_for_user(task_id, user.id, db)

    if not task:
        return redirect_page("/tasks", "Task not found")

    task.iscompleted = not task.iscompleted
    db.commit()

    return redirect_page("/tasks", "Task status updated")


@app.post("/tasks/{task_id}/delete")
def delete_task(
    task_id: int,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    user = get_page_user(request, response, db)

    if not user:
        return redirect_page("/login", "Please log in to continue")

    task = get_task_for_user(task_id, user.id, db)

    if not task:
        return redirect_page("/tasks", "Task not found")

    db.delete(task)
    db.commit()

    return redirect_page("/tasks", "Task deleted successfully")


@app.post("/refresh")
def refresh_token(
    request: Request,
    db: Session = Depends(get_db)
):
    token = request.cookies.get("refresh_token")

    if not token:
        response = redirect_page("/login", "Please log in again")
        clear_auth_cookies(response)
        return response

    try:
        payload = decode_token(token, "refresh")
    except HTTPException:
        response = redirect_page("/login", "Your session has expired")
        clear_auth_cookies(response)
        return response

    user_id = payload.get("sub")

    if not user_id or not user_id.isdigit():
        response = redirect_page("/login", "Please log in again")
        clear_auth_cookies(response)
        return response

    user = db.query(User).filter(User.id == int(user_id)).first()

    if not user:
        response = redirect_page("/login", "Please log in again")
        clear_auth_cookies(response)
        return response

    response = redirect_page("/dashboard", "Session refreshed")
    set_auth_cookies(response, user.id)

    return response


@app.post("/logout")
def logout():
    response = RedirectResponse("/login", status_code=303)
    clear_auth_cookies(response)
    response.headers["Cache-Control"] = "no-store"

    return response
