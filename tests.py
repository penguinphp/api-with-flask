from coverage import coverage
cov = coverage(omit=['env/*', 'tests.py'])
cov.start()

import unittest

from peewee import *
from models import User, Todo

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

    def tearDown(self):
        """Close DB"""
        TEST_DB.drop_tables(MODELS)
        TEST_DB.close()

    def test_user_create(self):
        """Create User / 2 Entries"""
        self.assertEqual(User.select().count(), 2)

    def test_user_create_two(self):
        """Create User / 2 Entries"""
        self.assertEqual(User.select().count(), 2)


if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    """Shows coverage report"""
    print("\n\nCoverage Report:\n")
    cov.report(show_missing=True)
    cov.erase()
