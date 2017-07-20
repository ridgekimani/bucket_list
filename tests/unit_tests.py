"""
This module is for testing some of the
implementations that will be used through out the app
"""

import datetime
import unittest
from .. app import DB, app

from flask_testing import TestCase


def load_data():
    """
    This function is used to load data that will be used for the tests
    :return:
    """
    data = {
        'test@user.com': 'test_password',
        'buckets': [
            {'user': 'test@user.com', 'bucket_name': 'test_bucket',
             'description': 'Test description', 'category': 'Health',
             'created': datetime.date(2017, 7, 19), 'key': '00000000'}
        ],
        'activities': [
            {'user': 'test@user.com', 'description': 'Test activity',
             'created': datetime.date(2017, 7, 19),
             'activity_key': '11111111', 'key': '00000000'}
        ]
    }

    return data


class TestLoginTestCases(TestCase):
    """
    This class is used to test cases that can an occur while trying to login
    This includes:
        wrong password
        incorrect email
    """

    def create_app(self):
        """
        The initial app configuration
        :return: app
        """
        DB['test@email.com'] = 'test_password'
        return app

    def test_home_page_redirect(self):
        """
        Tests that home page redirects to login
        :return: redirect
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_get_request(self):
        """
        Tests that the login get request works
        :return: 200
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_details(self):
        """
        Tests that correct credentials returns a success json response
        :return: success
        """
        response = self.client.post('/login/',
                                    data=dict(email='test@email.com', password='test_password'))
        self.assertEqual(response.json, dict(success='Authenticated successfully'))

    def test_login_with_wrong_email(self):
        """
        Test that wrong email returns a error json response
        :return: error
        """
        response = self.client.post('/login/',
                                    data=dict(email='test_wrong_email',
                                              password='test_password'))
        self.assertEqual(response.json,
                         dict(error='Email not found. Please sign up to continue'))

    def test_login_with_wrong_password(self):
        """
        Test that wrong password returns an error json response
        :return: error
        """
        response = self.client.post('/login/',
                                    data=dict(email='test@email.com',
                                              password='test_wrong_password'))
        self.assertEqual(response.json, dict(error='Incorrect password'))


class TestLogOutTestCase(unittest.TestCase):
    """
    This test class tests the logout functionality
    """
    def setUp(self):
        """
        The initial app configuration
        :return: app
        """
        DB['test@email.com'] = 'test_password'
        self.app = app.test_client()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = 'test@email.com'

    def test_logout_test_case(self):
        """
        The only test case that tests if a user can log out
        :return: 200
        """
        response = self.app.get('/logout/')
        self.assertEqual(response.status_code, 302)


class TestSignUpTestCases(TestCase):

    """
    This class is used to test cases that can an occur while trying to sign up
    This includes:
        existing email
        wrong passwords
        unfilled details

    """

    def create_app(self):
        """
        The initial app configuration
        :return: app
        """
        DB['test@email.com'] = 'test_password'
        return app

    def test_signup_get_request(self):
        """
        Test signup url returns a 200 status code for get request
        :return:
        """
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_signup_with_clean_data(self):
        """
        Test signup account with data that has not been used and is clean
        :return: success
        """
        response = self.client.post('/register/',
                                    data=dict(email='test@em.com',
                                              password='test_password',
                                              confirm_password='test_password'))
        self.assertEqual(response.json, {'success': 'Account created successfully'})

    def test_signup_with_existing_data(self):
        """
        Test signup account with existing data
        :return: error
        """
        response = self.client.post('/register/',
                                    data=dict(email='test@email.com',
                                              password='test_password',
                                              confirm_password='test_password'))
        self.assertEqual(response.json, {'error': 'User already exists with that email'})

    def test_signup_with_invalid_data(self):
        """
        Test signup with data that will be invalidated.
        This includes short email, short password
        :return: false
        """
        response = self.client.post('/register/', data={'email': 'kim'})
        self.assertEqual(response.json, {'error': 'email too short.'
                                                  ' Please enter more than 4 characters'})
        response = self.client.post('/register/', data={'email': 'test@email.com',
                                                        'password': 'pass'})
        self.assertEqual(response.json, {'error': 'Please enter more than '
                                                  '8 characters for your password'})


class TestBucketCRUDOperations(unittest.TestCase):
    """
    Test class is used to test the CRUD operations of a user if he/she is logged in
    This functionality includes:
            create bucket
            read bucket
            update bucket
            delete bucket
    """
    def setUp(self):
        self.app = app.test_client()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = 'test@user.com'

        DB['buckets'] = [
            {'user': 'test@user.com', 'bucket_name': 'test_bucket',
             'description': 'Test description',
             'category': 'Health', 'created': datetime.date(2017, 7, 19), 'key': '00000000'}
        ]

        DB['activities'] = [
            {'user': 'test@user.com', 'description': 'Test activity',
             'created': datetime.date(2017, 7, 19), 'activity_key': '11111111', 'key': '00000000'}
        ]

    def test_create_bucket_test_cases(self):
        """
        Test for both post and get request for the create bucket view
        :return: 200
        """
        response = self.app.get('/create_bucket/')
        self.assertEqual(response.status_code, 200)

        data = dict(bucket=True, email='test@email.com', bucket_name='test_bucket', category='6',
                    description='Test description')
        response = self.app.post('/create_bucket/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_read_bucket_test_cases(self):
        """
        Test the get request for the read bucket view
        :return: 200
        """
        response = self.app.get('/view_buckets/')
        self.assertEqual(response.status_code, 200)

    def test_update_bucket_test_cases(self):
        """
        Test for the post and get request for the update bucket view
        :return: 200
        """
        response = self.app.get('/update_bucket/')
        self.assertEqual(response.status_code, 302)
        response = self.app.get('/update_bucket/?key=00000000')
        self.assertEqual(response.status_code, 200)
        data = {'bucket_name': 'Test bucket', 'key': '000000'}
        response = self.app.post("/update_bucket/?key='00000000'", data=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_test_cases(self):
        """
        Test for the post request for the delete view
        :return:
        """
        response = self.app.delete('/delete/', data=dict(key='00000000', bucket='true'))
        self.assertEqual(response.status_code, 200)


class TestActivityCRUDOperations(unittest.TestCase):
    """
    Test class is used to test the CRUD operations of a user if he/she is logged in
    This functionality includes:
            create activity
            read activity
            update activity
            delete activity
    """
    def setUp(self):
        self.app = app.test_client()
        with self.app as app_:
            with app_.session_transaction() as sess:
                sess['user'] = 'test@user.com'

        DB['activities'] = [
            {'user': 'test@user.com', 'description': 'Test activity',
             'created': datetime.date(2017, 7, 19),
             'activity_key': '11111111', 'key': '00000000'}
        ]

    def test_create_activity_test_cases(self):
        """
        Test for the create activity post request
        :return: 200
        """
        data = dict(activity=True, text='Test activity', key='00000000')
        response = self.app.post('/add_activity/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_read_activity_test_cases(self):
        """
        Test for the read activity get request
        :return: 200
        """
        response = self.app.get("/view_activities/?key='00000000'")
        self.assertEqual(response.status_code, 200)

    def test_update_activity_test_cases(self):
        """
        Test for the update activity post and get request
        :return: 200
        """
        data = dict(description='Awesome description', key='00000000', activity_key='11111111')
        response = self.app.get('/update_activity/?key=0000000011111111')
        self.assertEqual(response.status_code, 200)
        response = self.app.post('/update_activity/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_delete_activity_test_cases(self):
        """
        Test for the delete post request
        :return:
        """
        data = {'key': '00000000', 'activity_key': '11111111', 'activity': 'true'}
        response = self.app.delete('/delete/', data=data)
        self.assertEqual(response.status_code, 200)
        data.pop('key')
        response = self.app.delete('/delete/', data=data)
        self.assertEqual(response.status_code, 500)


class TestBucketCRUDOperationsWithNoSessions(TestCase):
    """
    Test class is used to test the CRUD operations of a user if he/she is NOT logged in
    This functionality includes:
            create BUCKET
            read BUCKET
            update BUCKET
            delete BUCKET
    """

    def create_app(self):
        """
        The initial app configuration
        :return: app
        """
        return app

    def test_create_bucket(self):
        """
        Test create bucket post and get redirects
        :return: 302
        """
        response = self.client.get('/create_bucket/')
        self.assertEqual(response.status_code, 302)
        data = dict(bucket=True, email='test@email.com', bucket_name='test_bucket', category='6',
                    description='Test description')
        response = self.client.post('/create_bucket/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_data(self):
        """
        Test view bucket get redirects
        :return: 302
        """
        response = self.client.get('/view_buckets/')
        self.assertEqual(response.status_code, 302)

    def test_update_data(self):
        """
        Test update bucket post and get redirects
        :return: 302
        """
        response = self.client.get('/update_bucket/')
        self.assertEqual(response.status_code, 302)

    def test_delete_data(self):
        """
         Test delete bucket post and get redirects
         :return: 302
         """
        response = self.client.delete('/delete/', data={'bucket': 'true'})
        self.assertEqual(response.status_code, 302)


class TestActivityCRUDOperationsWithNoSessions(TestCase):
    """
    Test class is used to test the CRUD operations of a user if he/she is NOT logged in
    This functionality includes:
            create ACTIVITY
            read ACTIVITY
            update ACTIVITY
            delete ACTIVITY
    """
    def create_app(self):
        """
        The initial app configuration
        :return: app
        """
        return app

    def test_create_activity(self):
        """
        Test create activity post and get request redirects
        :return: 302
        """
        response = self.client.post('/add_activity/', data={'description': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_read_activity(self):
        """
        Test view activity get request redirects
        :return: 302
        """
        response = self.client.get('/view_activities/?key=567890')
        self.assertEqual(response.status_code, 302)

    def test_update_activity(self):
        """
        Test update activity post and get request redirects
        :return: 302
        """
        response = self.client.get('/update_activity/?key=67890')
        self.assertEqual(response.status_code, 302)
        response = self.client.post('/update_activity/', data={'description': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_delete_activity(self):
        """
        Test delete activity post request redirects
        :return: 302
        """
        response = self.client.delete('/delete/', data={'activity': 'true'})
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
