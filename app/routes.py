from functools import wraps

from flask import Blueprint, jsonify, request

from .task_manager import TaskManager
from .utils import log_to_file

main = Blueprint("main", __name__)
tasks = TaskManager()  # global singleton for this micro demo

# ---------------------------------------------------------------- helpers
def json_required(fn):
    """Decorator forcing a JSON body."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify(error="JSON body required"), 400
        return fn(*args, **kwargs)
    return wrapper

# ---------------------------------------------------------------- routes
@main.route("/")
def hello():
    return jsonify(message="Hello, world!")


@main.route("/greet")
def greet():
    name = request.args.get("name", "Guest")
    return jsonify(message=f"Hello, {name}!")


@main.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks=tasks.list_tasks())


@main.route("/tasks", methods=["POST"])
@json_required
def add_task():
    description = request.get_json().get("description")
    if not description:
        return jsonify(error="Description required"), 400
    task = tasks.add_task(description)
    return jsonify(task=task), 201


@main.route("/log", methods=["POST"])
@json_required
def log_message():
    message = request.get_json().get("message")
    if not message:
        return jsonify(error="Message required"), 400
    log_to_file(message)
    return jsonify(status="logged")
