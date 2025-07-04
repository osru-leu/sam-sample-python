import unittest
from app import create_app


class RoutesTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app().test_client()

    # ---------- root --------------------------------------------------------

    def test_root_hello(self):
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, world!"})

    # ---------- /greet ------------------------------------------------------

    def test_greet_default(self):
        resp = self.app.get("/greet")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, Guest!"})

    def test_greet_named(self):
        resp = self.app.get("/greet?name=Alice")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"message": "Hello, Alice!"})

    # ---------- /tasks ------------------------------------------------------

    def test_add_and_list_tasks(self):
        # add a task
        post = self.app.post("/tasks", json={"description": "Write tests"})
        self.assertEqual(post.status_code, 201)
        self.assertEqual(post.json["task"]["description"], "Write tests")

        # list tasks
        get = self.app.get("/tasks")
        self.assertEqual(get.status_code, 200)
        self.assertTrue(any(t["description"] == "Write tests"
                            for t in get.json["tasks"]))

    def test_add_task_requires_description(self):
        post = self.app.post("/tasks", json={})
        self.assertEqual(post.status_code, 400)

    # ---------- /log --------------------------------------------------------

    def test_log_message(self):
        post = self.app.post("/log", json={"message": "Unit‑test entry"})
        self.assertEqual(post.status_code, 200)
        self.assertEqual(post.json, {"status": "logged"})

    def test_log_message_requires_json(self):
        post = self.app.post("/log", data="plain text")
        self.assertEqual(post.status_code, 400)


if __name__ == "__main__":
    unittest.main()
