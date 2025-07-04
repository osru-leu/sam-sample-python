class TaskManager:
    """A tiny in‑memory task list."""

    def __init__(self) -> None:
        self.reset()  # start with a clean state

    def add_task(self, description: str) -> dict:
        task = {"id": self._next_id, "description": description}
        self._tasks.append(task)
        self._next_id += 1
        return task

    def list_tasks(self) -> list[dict]:
        return self._tasks.copy()  # shallow copy to protect internal state

    def reset(self) -> None:
        """Clear all tasks and reset ID counter (used in unit tests)."""
        self._tasks: list[dict] = []
        self._next_id: int = 1