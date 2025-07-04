import unittest
from app import create_app

class HelloWorldTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_hello_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, world!"})

if __name__ == '__main__':
    unittest.main()
