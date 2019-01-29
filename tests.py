from coverage import coverage
cov = coverage(omit=['env/*', 'tests.py'])
cov.start()

import unittest

from peewee import *
from models import User, Todo
from app import app

MODELS = [User, Todo]

TEST_DB = SqliteDatabase(':memory:')

TEST_USER = {
    'username': 'test',
    'email': 'test@test.com',
    'password': 'password',
    'verify_password': 'password'
}

TEST_USER2 = {
    'username': 'test2',
    'email': 'test2@test2.com',
    'password': 'password',
    'verify_password': 'password'
}


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Connect to DB"""
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.connect()
        TEST_DB.create_tables(MODELS)
        self.test_user = User.create_user('test', 'test@test.com', 'password')
        self.test_user = User.create_user('test2', 'test2@test2.com', 'password')
        self.client = app.test_client()

    def tearDown(self):
        """Close DB"""
        TEST_DB.drop_tables(MODELS)
        TEST_DB.close()

    def test_create_user(self):
        """Create User / 2 Entries"""
        self.assertEqual(User.select().count(), 2)
        self.assertNotEqual(
            User.select().get().password,
            'password123'
        )

    def test_create_user_two(self):
        """Create User / 2 Entries"""
        self.assertEqual(User.select().count(), 2)
        self.assertNotEqual(
            User.select().get().password,
            'password12'
        )

    def test_set_password(self):
        self.assertEqual(User.select().count(), 2)
        self.assertNotEqual(
            User.select().get().password,
            'password123'
        )

    def test_todo_get(self):
        """Test Get"""
        self.response = self.client.get('http://0.0.0.0:8000/api/v1/todos')
        self.assertEqual(self.response.status_code, 200)

    def test_todo_put(self):
        """Test Put"""
        self.response = self.client.get('http://0.0.0.0:8000/api/v1/todos/1')
        self.assertEqual(self.response.status_code, 404)

    def test_todo_delete(self):
        """Test Delete"""
        self.response = self.client.delete('http://0.0.0.0:8000/api/v1/todos/1')
        self.assertEqual(self.response.status_code, 204)


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_my_todos(self):
        self.response = self.client.get("/")
        self.assertEqual(self.response.status_code, 200)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    """Shows coverage report"""
    print("\n\nCoverage Report:\n")
    cov.report()
    cov.erase()
