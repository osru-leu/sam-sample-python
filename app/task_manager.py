class TaskManager:
    """A very small in‑memory task list."""

    def __init__(self) -> None:
        self._tasks: list[dict] = []
        self._next_id: int = 1

    # ----- public API -------------------------------------------------------

    def add_task(self, description: str) -> dict:
        task = {"id": self._next_id, "description": description}
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[dict]:
        return self._tasks.copy()          # return a shallow copy
