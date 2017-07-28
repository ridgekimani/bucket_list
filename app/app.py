"""
This is the bucket list main app.
It handles all activities that will be used  within the app
This includes: login, CRUD operations of buckets and activities
"""


from app.abstract_class import AbstractFeatures, DB

from flask import request, render_template, Flask, jsonify, make_response, redirect, session

from flask.views import View

app = Flask(__name__)

app.secret_key = '1db2650244d04d998ef3ff97469e85b4'


CATEGORIES = [
    {'1': 'Travel'},
    {'2': 'Health'},
    {'3': 'Wealth'},
    {'4': 'Career'},
    {'5': 'Relationship'},
    {'6': 'Self Growth'},
    {'7': 'General'}
]


@app.route('/', methods=['GET'])
def home():
    """
    Redirects to register
    :return:
    """
    return redirect('/register/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    """
    This function is used to register a new user. It
    contains validation to an existing user
    :return: 200
    """
    if request.method == 'GET':
        return render_template('registration/register.html')

    if request.method == 'POST':
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')

        if len(email) < 5:
            return make_response(jsonify({'error': 'email too short. '
                                                   'Please enter more than 4 characters'}), 400)

        if len(password) < 8:
            return make_response(jsonify({'error': 'Please enter more than '
                                                   '8 characters for your password'}), 400)

        if email in DB.keys():
            return make_response(jsonify({'error': 'User already exists with that email'}), 409)

        DB[email] = password
        session['user'] = email
        return jsonify({'success': 'Account created successfully'})


@app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    This function is used to login a user
    The user is created a session to log into
    :return: json response

    """

    if request.method == 'GET':
        return render_template('registration/login.html')

    if request.method == 'POST':
        data = request.form.to_dict()
        email = data.get('email')
        password = data.get('password')

        if email not in DB.keys():
            return make_response(jsonify({'error': 'Email not found. '
                                                   'Please sign up to continue'}), 500)

        for key, value in DB.items():
            if key == email:
                if value == password:
                    session['user'] = email
                    return jsonify({'success': 'Authenticated successfully'})
                else:
                    return make_response(jsonify({'error': 'Incorrect password'}), 401)


@app.route('/logout/', methods=['GET'])
def logout():
    """
    Logs out a user
    :return:
    """
    session.pop('user', None)
    return redirect('/login/')


class CreateBucket(AbstractFeatures, View):
    """
    This function is used to create bucket data and save it to the databas
    """

    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """

        def get():
            """
            This method is used to get data from the database and render it to a template
            :return: response
            """
            if 'user' in session.keys() and 'user' in session.keys() is not None:
                return render_template('create_bucket.html', page='Create Bucket', data=CATEGORIES)
            else:
                return redirect('/login/')

        def post():
            """
            This method is used to post data to the database and return a response
            :return: response
            """
            email = session.get('user')

            if not email:
                return redirect('/login/')

            data = request.form.to_dict()
            bucket_name = data.get('bucket_name')
            description = data.get('description')
            value = data.get('category')
            category = ''

            for category_ in CATEGORIES:
                for key, val in category_.items():
                    if key == value:
                        category = val

            data = dict(bucket=True, email=email, bucket_name=bucket_name, category=category,
                        description=description)
            response = self.create_data(**data)
            if response.message:
                return make_response(jsonify({'success': 'Bucket Created successfully'}), 200)

        if request.method == 'GET':
            return get()

        elif request.method == 'POST':
            return post()


class ViewBucket(AbstractFeatures, View):
    """
    This class implements functionality of viewing the
    bucket's details.
    It implements a get request to render the details
    """

    methods = ['GET']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """
        if 'user' in session.keys() and 'user' in session.keys() is not None:
            details = self.read_data(email=session.get('user'), bucket=True)
            if details:
                new_details = {}
                for key_, value_ in enumerate(details):
                    new_details[key_] = value_
                return render_template('view_buckets.html', details=new_details, data=True,
                                       page='View Buckets')
            return render_template('view_buckets.html', data=False, page='View Buckets')
        else:
            return redirect('/login/')


class UpdateBucket(AbstractFeatures, View):
    """
    This class is used to update a bucket.
    It implements a get request to render the template and
    a post request to update the bucket
    """

    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """

        def get():
            """
            This method is used to get bucket data from the database
            and render it to a template
            :return: response
            """
            unique_key = request.args.get('key')

            if not unique_key:
                return redirect('/view_buckets/')

            if 'user' in session.keys() and 'user' in session.keys() is not None:
                data = self.get_specific_data(key=unique_key,
                                              email=session.get('user'), bucket=True)
                if data:
                    new_details = {}
                    for key_, value_ in enumerate(data):
                        new_details[key_] = value_

                    return render_template(
                        'update_bucket.html', page='Update Bucket',
                        data=new_details, categories=CATEGORIES, unique_key=unique_key)
            else:
                return redirect('/login/')

        def post():
            """
            This method is used to post updated bucket data to  the database and
                return a response
            :return: response
            """
            email = session.get('user')

            if not email:
                return redirect('/login/')

            data = request.form.to_dict()
            bucket_name = data.get('bucket_name')
            description = data.get('description')
            value = data.get('category')
            unique_key = data.get('key')
            category = ''

            for category_ in CATEGORIES:
                for key, val in category_.items():
                    if key == value:
                        category = val

            data = dict(bucket=True, email=email, bucket_name=bucket_name,
                        category=category, key=unique_key,
                        description=description)

            response = self.update_data(**data)

            if response.message:
                return make_response(jsonify({'success': 'Bucket Updated successfully'}), 200)

            else:
                return make_response(jsonify({'error': self.error_message}), 500)

        if request.method == 'GET':
            return get()

        elif request.method == 'POST':
            return post()


class AddActivity(AbstractFeatures, View):
    """
    This class handles adding activities of a user
    This method uses a post request to add it.
    """
    methods = ['POST']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """
        email = session.get('user')

        if not email:
            return redirect('/login/')

        data = request.form.to_dict()
        unique_key = data.get('key')
        description = data.get('text')
        if not unique_key:
            return make_response(jsonify({'error': 'Please select a specific bucket'}), 500)

        if not description:
            return make_response(jsonify({'error': 'Please enter your activities'}), 500)

        data = dict(activity=True, email=email, description=description, key=unique_key)

        response = self.create_data(**data)
        if response.message:
            return make_response(jsonify({'success': 'Activity added successfully'}))


class ViewActivities(AbstractFeatures, View):
    """
    This class implements functionality of viewing the
    activity's details.
    It implements a get request to render the details
    """

    methods = ['GET']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """
        key = request.args.get('key')
        if not key:
            return redirect('/view_buckets/')

        if 'user' in session.keys() and 'user' in session.keys() is not None:
            try:
                details, bucket_name = self.read_data(
                    email=session.get('user'), activity=True, key=key)
                new_details = {}
                for key_, value_ in enumerate(details):
                    new_details[key_] = value_

                return render_template('view_activities.html',
                                       details=new_details, data=True, page='View Buckets',
                                       bucket=bucket_name)

            except ValueError:
                return render_template('view_activities.html', data=False, page='View Buckets')
        else:
            return redirect('/login/')


class UpdateActivity(AbstractFeatures, View):
    """
    This class is used to update activity that will
    be selected by the user. This class uses two
    view methods. POST and GET
    """
    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """
        def get():
            """
            This method is used to get activity data from the database and render to a template
            :return: response
            """
            unique_key = request.args.get('key')

            if not unique_key or len(unique_key) != 16:
                return redirect('/view_buckets/')

            key = unique_key[:8]
            activity_key = unique_key[8:]

            if 'user' in session.keys() and 'user' in session.keys() is not None:
                data = self.get_specific_data(key=key, email=session.get('user'), activity=True,
                                              activity_key=activity_key)
                if data:
                    new_details = {}
                    for key_, value_ in enumerate(data):
                        new_details[key_] = value_

                    return render_template('update_activity.html',
                                           page='Update Activity', data=new_details,
                                           unique_key=key, activity_key=activity_key)
                else:
                    return render_template('update_activity.html', page='Update Activity')
            else:
                return redirect('/login/')

        def post():
            """
            This method is used to post activity data to the database
            :return: response
            """
            email = session.get('user')

            if not email:
                return redirect('/login/')

            data = request.form.to_dict()
            key = data.get('key')
            description = data.get('description')
            activity_key = data.get('activity_key')

            data = dict(activity=True, email=email,
                        key=key, description=description, activity_key=activity_key)

            response = self.update_data(**data)

            if response.message:
                return make_response(jsonify({'success': 'Activity Updated successfully'}), 200)

        if request.method == 'GET':
            return get()

        elif request.method == 'POST':
            return post()


class DeleteData(AbstractFeatures, View):
    """
    This class is used to delete data when a user selects it
    This data includes activities and buckets
    """

    methods = ['DELETE']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """
        email = session.get('user')

        if not email:
            return redirect('/login/')

        data = request.form.to_dict()
        key = data.get('key')
        bucket = data.get('bucket')
        activity = data.get('activity')
        activity_key = data.get('activity_key')

        if not key:
            return make_response(jsonify(
                {'error': 'Please select a specific bucket or activity'}), 500)

        def delete_bucket():
            """
            Function that handles delete bucket
            :return: json response
            """
            values = dict(key=key, bucket=True)
            response = self.delete_data(**values)

            if response.message:
                return make_response(jsonify({'success': 'Bucket deleted successfully'}))

        def delete_activity():
            """
            Function that handles delete activity
            :return: json response
            """
            values = dict(key=key, activity=True, activity_key=activity_key)
            response = self.delete_data(**values)

            if response.message:
                return make_response(jsonify({'success': response.message}))

        if bucket == 'true':
            return delete_bucket()

        if activity == 'true':
            return delete_activity()


app.add_url_rule('/create_bucket/', view_func=CreateBucket.as_view('create_bucket'))
app.add_url_rule('/view_buckets/', view_func=ViewBucket.as_view('view_buckets'))
app.add_url_rule('/update_bucket/', view_func=UpdateBucket.as_view('update_bucket'))
app.add_url_rule('/add_activity/', view_func=AddActivity.as_view('add_activity'))
app.add_url_rule('/view_activities/', view_func=ViewActivities.as_view('view_activities'))
app.add_url_rule('/update_activity/', view_func=UpdateActivity.as_view('update_activity'))
app.add_url_rule('/delete/', view_func=DeleteData.as_view('delete_data'))
