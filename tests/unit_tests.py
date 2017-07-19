import unittest
from .. app import db, app, AbstractFeatures

from flask_testing import TestCase


class TestLoginTestCases(TestCase):
    """
    This class is used to test cases that can an occur while trying to login
    This includes:
        wrong password
        incorrect username
    """

    def create_app(self):
        db['test@email.com'] = 'test_password'
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
        :return: 200
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
        response = self.client.post('/login/', data=dict(email='test@email.com', password='test_password'))
        self.assertEqual(response.json, dict(success='Authenticated successfully'))

    def test_login_with_wrong_username(self):
        """
        Test that wrong username returns a error json response
        :return: error
        """
        print("----------Test login with wrong username------------")
        response = self.client.post('/login/', data=dict(email='test_wrong_username', password='test_password'))
        self.assertEqual(response.json, dict(error='Username not found. Please sign up to continue'))

    def test_login_with_wrong_password(self):
        """
        Test that wrong password returns an error json response
        :return: error
        """
        print("----------Test login with wrong password------------")
        response = self.client.post('/login/', data=dict(email='test@email.com', password='test_wrong_password'))
        self.assertEqual(response.json, dict(error='Incorrect password'))


class TestLogOutTestCase(unittest.TestCase):
    """
    This test class tests the logout functionality
    """
    def setUp(self):
        db['test@email.com'] = 'test_password'
        self.app = app.test_client()
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test@email.com'

    def test_logout_test_case(self):
        """
        The only test case that tests if a user can log out
        :return: 200
        """
        print("----------Test if a user can log out------------")
        response = self.app.get('/logout/')
        self.assertEqual(response.status_code, 302)


class TestSignUpTestCases(TestCase):

    """
    This class is used to test cases that can an occur while trying to sign up
    This includes:
        existing username
        wrong passwords
        unfilled details

    """

    def create_app(self):
        db['test@email.com'] = 'test_password'
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
        response = self.client.post('/register/', data=dict(email='test@em.com', password='test_password',
                                                            confirm_password='test_password'))
        self.assertEqual(response.json, {'success': 'Account created successfully'})

    def test_signup_with_existing_data(self):
        """
        Test signup account with existing data
        :return: error
        """
        print("---------Test for signup with existing username---------------")
        response = self.client.post('/register/', data=dict(email='test@email.com', password='test_password',
                                                            confirm_password='test_password'))
        self.assertEqual(response.json, {'error': 'User already exists with that username'})

    def test_signup_with_wrong_confirm_password(self):
        """
        Test signup account with passwords that don't match
        :return: false
        """
        print("---------Test for signup with wrong confirm password---------------")
        response = self.client.post('/register/', data=dict(email='test_use1',
                                                            password='test_password', confirm_password='test_pass'))
        self.assertEqual(response.json, {'error': 'Passwords do not match'})

    def test_signup_post_request_with_no_data(self):
        """
        Test that signup with no data will raise errors
        :return: false
        """
        print("-------------Test signup post request with no data raises errors----------")
        response = self.client.post('/register/', data={})
        self.assertEqual(response.json, {'error': 'Please enter your email'})
        response = self.client.post('/register/', data={'email': 'test_use1'})
        self.assertEqual(response.json, {'error': 'Please enter your password'})
        response = self.client.post('/register/', data={'email': 'test_use1', 'password': 'test_password'})
        self.assertEqual(response.json, {'error': 'Please confirm your password'})

    def test_signup_with_invalid_data(self):
        """
        Test signup with data that will be invalidated.
        This includes short username, short password
        :return: false
        """
        print("------------Test for signup with short username----------------")
        response = self.client.post('/register/', data={'email': 'kim'})
        self.assertEqual(response.json, {'error': 'Username too short. Please enter more than 4 characters'})
        print("------------Test for signup with short password ----------------")
        response = self.client.post('/register/', data={'email': 'test@email.com', 'password': 'pass'})
        self.assertEqual(response.json, {'error': 'Please enter more than 8 characters for your password'})


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
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test@user.com'


    def test_create_bucket_test_cases(self):
        """
        Test for both post and get request for the create bucket view
        :return: 200
        """
        print('-------_Test for create get request------------')
        response = self.app.get('/create_bucket/')
        self.assertEqual(response.status_code, 200)

        data = dict(bucket=True, username='test@email.com', bucket_name='test_bucket', category='6',
                    description='Test description')
        print('--------Test for create post request------------')
        response = self.app.post('/create_bucket/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_read_bucket_test_cases(self):
        """
        Test the get request for the read bucket view
        :return: 200
        """
        print("------------Test for view bucket -----------")
        response = self.app.get('/view_buckets/')
        self.assertEqual(response.status_code, 200)

    def test_update_bucket_test_cases(self):
        """
        Test for the post and get request for the update bucket view
        :return: 200
        """
        x = AbstractFeatures()
        print(x.key)
        print("----------Test for update bucket get request without any params----------")
        response = self.app.get('/update_bucket/')
        self.assertEqual(response.status_code, 302)
        print("---------Test for update bucket get with params------------")
        response = self.app.get("/update_bucket/")

    def test_delete_test_cases(self):
        """
        Test for the post request for the delete view
        :return:
        """
        print("-----------Test for delete bucket ---------------")
        response = self.app.post('/delete/', data=dict(key='00000000', bucket='true'))
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
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user'] = 'test@user.com'

    def create_activity_test_cases(self):
        """
        Test for the create activity post request
        :return: 200
        """
        print("----------Test for create activity post request----------")
        data = dict(activity=True, text='Test activity')
        response = self.app.post('/add_activity/', data=data)
        self.assertEqual(response.status_code, 200)

    def read_activity_test_cases(self):
        """
        Test for the read activity get request
        :return: 200
        """
        print("--------Test for read activity get request----------")
        response = self.app.get("/view_activities/?key='00000000'")
        self.assertEqual(response.status_code, 200)

    def update_activity_test_cases(self):
        """
        Test for the update activity post and get request
        :return: 200
        """
        print("--------Test for update activity get request-------------")
        response = self.app.get("/update_activity/?key='0000000011111111'")


    def delete_activity_test_cases(self):
        """
        Test for the delete post request
        :return:
        """
        print("----------Test for delete activity -------------")
        data = {'key': '00000000', 'activity_key': '11111111', 'activity': 'true'}
        response = self.app.post('/delete/', data=data)
        self.assertEqual(response.status_code, 200)


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
        return app

    def test_create_bucket(self):
        """
        Test create bucket post and get redirects
        :return: 302
        """
        print('-------_Test for create get request redirects------------')
        response = self.client.get('/create_bucket/')
        self.assertEqual(response.status_code, 302)
        data = dict(bucket=True, username='test@email.com', bucket_name='test_bucket', category='6',
                    description='Test description')
        print('--------Test for create post request')
        response = self.client.post('/create_bucket/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_read_data(self):
        """
        Test view bucket get redirects
        :return: 302
        """
        print("------------Test for view bucket redirects-----------")
        response = self.client.get('/view_buckets/')
        self.assertEqual(response.status_code, 302)

    def test_update_data(self):
        """
        Test update bucket post and get redirects
        :return: 302
        """
        print("----------Test for update bucket get request redirects----------")
        response = self.client.get('/update_bucket/?key=6789000')
        self.assertEqual(response.status_code, 302)

    def test_delete_data(self):
        """
         Test delete bucket post and get redirects
         :return: 302
         """
        print("---------Test for delete bucket post redirects------------")
        response = self.client.post('/delete/', data={'bucket': 'true'})
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
        return app

    def test_create_activity(self):
        """
        Test create activity post and get request redirects
        :return: 302
        """
        print("-----------Test create activity post request redirects-----------")
        response = self.client.post('/add_activity/', data={'description': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_read_activity(self):
        """
        Test view activity get request redirects
        :return: 302
        """
        print('------Test view activity get request redirects----------')
        response = self.client.get('/view_activities/?key=567890')
        self.assertEqual(response.status_code, 302)

    def test_update_activity(self):
        """
        Test update activity post and get request redirects
        :return: 302
        """
        print('---------Test update activity get request redirects-----------')
        response = self.client.get('/update_activity/?key=67890')
        self.assertEqual(response.status_code, 302)
        print('---------Test update activity post request redirects-----------')
        response = self.client.post('/update_activity/', data={'description': 'test'})
        self.assertEqual(response.status_code, 302)

    def test_delete_activity(self):
        """
        Test delete activity post request redirects
        :return: 302
        """
        print('-----------Test delete activity post request------------')
        response = self.client.post('/delete/', data={'activity': 'true'})
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
