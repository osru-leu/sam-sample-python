from functools import wraps

from flask import Blueprint, jsonify, request

from .task_manager import TaskManager
from .utils import log_to_file

main = Blueprint("main", __name__)
tasks = TaskManager()  # global singleton for this tiny demo


# ---------- helpers ---------------------------------------------------------

def json_required(func):
    """Simple decorator enforcing a JSON request body."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.is_json:
            return jsonify(error="JSON body required"), 400
        return func(*args, **kwargs)
    return wrapper


# ---------- routes ----------------------------------------------------------

@main.route("/")
def hello() -> tuple[dict, int]:
    return jsonify(message="Hello, world!")


@main.route("/greet")
def greet() -> tuple[dict, int]:
    name = request.args.get("name", "Guest")
    return jsonify(message=f"Hello, {name}!")


@main.route("/tasks", methods=["GET"])
def get_tasks() -> tuple[dict, int]:
    return jsonify(tasks=tasks.list_tasks())


@main.route("/tasks", methods=["POST"])
@json_required
def add_task() -> tuple[dict, int]:
    description = request.get_json().get("description")
    if not description:
        return jsonify(error="Description required"), 400
    task = tasks.add_task(description)
    return jsonify(task=task), 201


@main.route("/log", methods=["POST"])
@json_required
def log_message() -> tuple[dict, int]:
    message = request.get_json().get("message")
    if not message:
        return jsonify(error="Message required"), 400
    log_to_file(message)
    return jsonify(status="logged")
