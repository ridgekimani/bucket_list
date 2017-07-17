from flask_testing import TestCase
from app import app, db


class TestLoginTestCases(TestCase):
    """
    This class is used to test cases that can an occur while trying to login
    This includes:
        wrong password
        incorrect username
    """

    def create_app(self):
        db['test_username'] = 'test_password'
        self.db = db
        return app

    def test_home_page_redirect(self):
        """
        Tests that home page redirects to login
        :return: redirect
        """
        print("-----Test that homepage redirects to login-----------")
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login_get_request(self):
        """
        Tests that the login get request works
        :return: true
        """
        print("-----Test login request returns a 200 status---------")
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_with_correct_details(self):
        """
        Tests that correct credentials returns a success json response
        :return: success
        """
        print("--------------Test login with correct credentials------------")
        response = self.client.post('/login/', data=dict(username='test_username', password='test_password'))
        self.assertEqual(response.json, dict(success='Authenticated successfully'))

    def test_login_with_wrong_username(self):
        """
        Test that wrong username returns a error json response
        :return: error
        """
        print("----------Test login with wrong username------------")
        response = self.client.post('/login/', data=dict(username='test_wrong_username', password='test_password'))
        self.assertEqual(response.json, dict(error='Username not found. Please sign up to continue'))

    def test_login_with_wrong_password(self):
        """
        Test that wrong password returns an error json response
        :return: error
        """
        print("----------Test login with wrong password------------")
        response = self.client.post('/login/', data=dict(username='test_username', password='test_wrong_password'))
        self.assertEqual(response.json, dict(error='Incorrect password'))


class TestSignUpTestCases(TestCase):

    """
    This class is used to test cases that can an occur while trying to sign up
    This includes:
        existing username
        wrong passwords
        unfilled details

    """

    def create_app(self):
        db['test_username'] = 'test_password'
        self.db = db
        return app

    def test_signup_get_request(self):
        """
        Test signup url returns a 200 status code for get request
        :return:
        """
        print("-----------Test that signup page returns a 200 status---------------")
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_signup_with_clean_data(self):
        """
        Test signup account with data that has not been used and is clean
        :return: success
        """
        print("---------Test for signup with unique and clean data---------------")
        response = self.client.post('/register/', data=dict(username='kim', password='ridge', confirm_password='ridge'))
        self.assertEqual(response.json, {'success': 'Account created successfully'})

    def test_signup_with_existing_data(self):
        """
        Test signup account with existing data
        :return: error
        """
        print("---------Test for signup with existing username---------------")
        response = self.client.post('/register/', data=dict(username='test_username', password='ridge',
                                                            confirm_password='ridge'))
        self.assertEqual(response.json, {'error': 'User already exists with that username'})

    def test_signup_with_wrong_confirm_password(self):
        """
        Test signup account with passwords that don't match
        :return: false
        """
        print("---------Test for signup with wrong confirm password---------------")
        response = self.client.post('/register/', data=dict(username='kim1', password='ridge', confirm_password='ri'))
        self.assertEqual(response.json, {'error': 'Passwords do not match'})

    def test_signup_post_request_with_no_data(self):
        """
        Test that signup with no data will raise errors
        :return: false
        """
        print("-------------Test signup post request with no data raises errors----------")
        response = self.client.post('/register/', data={})
        self.assertEqual(response.json, {'error': 'Please enter your username'})
        response = self.client.post('/register/', data={'username': 'kim1'})
        self.assertEqual(response.json, {'error': 'Please enter your password'})
        response = self.client.post('/register/', data={'username': 'kim1', 'password': 'pass'})
        self.assertEqual(response.json, {'error': 'Please confirm your password'})
