import os
import unittest
from unittest.mock import patch

from app import create_app
from app.routes import tasks          # global TaskManager instance
from app.utils import LOG_PATH


class RoutesTestCase(unittest.TestCase):
    # ----------------------------------------------------------- test setup
    def setUp(self) -> None:
        self.app = create_app().test_client()

        # reset shared state so every test starts clean
        tasks.reset()

        # remove any previous log output
        if LOG_PATH.exists():
            LOG_PATH.unlink()

    # -------------------------------------------------------------- /
    def test_root_hello(self):
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, world!"})

    # ----------------------------------------------------------- /greet
    def test_greet_default(self):
        resp = self.app.get("/greet")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, Guest!"})

    def test_greet_named(self):
        resp = self.app.get("/greet?name=Alice")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, Alice!"})

    # ----------------------------------------------------------- /tasks
    def test_add_and_list_tasks(self):
        post = self.app.post("/tasks", json={"description": "Write tests"})
        self.assertEqual(post.status_code, 201)
        self.assertEqual(post.json["task"]["description"], "Write tests")

        get = self.app.get("/tasks")
        self.assertEqual(get.status_code, 200)
        self.assertTrue(
            any(t["description"] == "Write tests" for t in get.json["tasks"])
        )

    def test_add_task_requires_description(self):
        post = self.app.post("/tasks", json={})
        self.assertEqual(post.status_code, 400)

    # -------------------------------------------------------------- /log
    def test_log_message(self):
        post = self.app.post("/log", json={"message": "Unit‑test entry"})
        self.assertEqual(post.status_code, 200)
        self.assertEqual(post.json, {"status": "logged"})

        # verify file content
        with open(LOG_PATH, encoding="utf-8") as fh:
            content = fh.read()
            self.assertIn("Unit‑test entry", content)

    def test_log_message_requires_json(self):
        post = self.app.post("/log", data="plain text")
        self.assertEqual(post.status_code, 400)


if __name__ == "__main__":
    unittest.main()