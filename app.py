import uuid

from datetime import date

from flask import request, render_template, Flask, jsonify, make_response, redirect, session

from flask.views import View

app = Flask(__name__)

app.secret_key = 'this is a secret'

DB = dict()

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
    Redirects to login
    :return:
    """
    return redirect('/login/')


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
                                                   'Please enter more than 4 characters'}), 500)

        if len(password) < 8:
            return make_response(jsonify({'error': 'Please enter more than '
                                                   '8 characters for your password'}), 500)

        if email in DB.keys():
            return make_response(jsonify({'error': 'User already exists with that email'}), 500)

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
                    return make_response(jsonify({'error': 'Incorrect password'}), 500)


@app.route('/logout/', methods=['GET'])
def logout():
    """
    Logs out a user
    :return:
    """
    session.pop('user', None)
    return redirect('/login/')


class AbstractFeatures(object):

    """
    This mixin class is used for most OOP functionality that will be used within the app
    This methods include:
     1. Create data for both buckets and activities
     2. Read data and return the data in a particular format for buckets and activities
     3. Delete Data for the buckets and activities
    It contains some accessor methods that can be used when subclassing this class

    Usage:
     from flask.views import View

     class CreateBucketView(AbstractFeatures, View):
        def dispatch(self, *args, **kwargs):
          return self.create_data(*args, **kwargs)

    """

    def __init__(self, *args, **kwargs):
        self.details = kwargs
        self.args = args
        self.message = None
        self.error_message = None
        self.email = None
        self.bucket_name = None
        self.description = None
        self.category = None
        self.bucket = False
        self.activity = False
        self.filtered = []
        self.key = None
        self.activity_key = None
        self.initialize()

    def initialize(self):
        """
        Maps arguments to keyword arguments and
        assigns the values to the attributes with the same name
        when the __init__ method is called
        :return: dict values
        """
        map(lambda x: self.details.update(dict(x, )), self.args)
        for key, value in self.details.items():
            setattr(self, key, value)

    def _create_data(self):
        """
        This private method is used to create data for both buckets and activities
        This method contains two methods, add_bucket and
        add_activity and the correct functionality is
        used when specifying if its a bucket or activity as an argument
        """
        def add_bucket():
            """
            This method is used to create bucket
            :return: self
            """

            value = uuid.uuid4()
            key = str(value)[:8]
            values = dict(user=self.email, bucket_name=self.bucket_name,
                          description=self.description, category=self.category,
                          created=date.today(), key=key)

            if 'buckets' in DB.keys():
                DB['buckets'].append(values)
            else:
                DB['buckets'] = [values]
            self.message = 'Data created successfully'
            return self

        def add_activity():
            """
            This method is used to create an activity
            :return: self
            """
            value = uuid.uuid4()
            key = str(value)[:8]
            values = dict(user=self.email, description=self.description,
                          created=date.today(), activity_key=key, key=self.key)

            if 'activities' in DB.keys():
                DB['activities'].append(values)

            else:
                DB['activities'] = [values]

            self.message = 'Data created successfully'
            return self

        if self.bucket:
            return add_bucket()

        elif self.activity:
            return add_activity()

    def _read_data(self):
        """
        Used to read buckets and activities of the current user
        :return: list of dictionaries containing this data
        """
        def read_buckets():
            """
            This method is used to read buckets
            :return: filtered_data
            """
            try:
                self.filtered = [item for item in DB['buckets'] if item['user'] == self.email]
                return self.filtered

            except KeyError:
                return []

        def read_activities():
            """
            This method is used to read activities
            :return: filtered_data
            """
            try:
                self.filtered = [item for item in DB['activities']
                                 if item['user'] == self.email and item['key'] == self.key]

                specific = self.get_specific_data(bucket=True, email=self.email, key=self.key)

                new_details = {}
                for key_, value_ in enumerate(specific):
                    new_details[key_] = value_

                val = ''
                for value in new_details.values():
                    for key, val in value.items():
                        if key == 'bucket_name':
                            break

                self.bucket_name = val
                return self.filtered, self.bucket_name

            except KeyError:
                return []

        if self.bucket:
            return read_buckets()

        elif self.activity:
            return read_activities()
        else:
            return False

    def _update_data(self):
        """
        Used to update data from buckets and activities
        :return: updated data
        """
        def update_bucket():
            """
            Used to update the bucket
            :return: self
            """
            bucket = [item for item in DB['buckets'] if item['key'] == self.key]
            new_details = {}
            for key_, value_ in enumerate(bucket):
                new_details[key_] = value_

            for values in new_details.values():
                values['bucket_name'] = self.bucket_name
                values['description'] = self.description
                values['category'] = self.category

            self.message = 'Bucket updated successfully'
            return self

        def update_activity():
            """
            Used to update the activity
            :return: self
            """
            activity = [item for item in DB['activities']
                        if item['key'] == self.key and item['activity_key'] == self.activity_key]

            new_details = {}
            for key_, value_ in enumerate(activity):
                new_details[key_] = value_

            for values in new_details.values():
                values['description'] = self.description

            self.message = 'Activity updated successfully'
            return self

        if self.bucket:
            return update_bucket()

        if self.activity:
            return update_activity()

    def _delete_data(self):

        def delete_bucket():
            DB['buckets'] = [item for item in DB['buckets'] if item['key'] != self.key]
            try:

                DB['activities'] = [item for item in DB['activities'] if item['key'] != self.key]
            except KeyError:
                pass

            self.message = 'Bucket deleted successfully'
            return self

        def delete_activity():
            DB['activities'] = [item for item in DB['activities']
                                if item['key'] != self.key and
                                item['activity_key'] != self.activity_key]

            self.message = 'Activity successfully deleted'
            return self

        if self.bucket:
            return delete_bucket()

        if self.activity:
            return delete_activity()

    def _get_specific_data(self):
        """
        This method is used to get specific data unit given the key and the email
        It is used while creating a bucket activity or updating the bucket
        :return:
        """
        def get_bucket():
            """
            Used to get a specific bucket and return it
            :return: specific_bucket
            """
            try:
                self.filtered = [item for item in DB['buckets']
                                 if item['user'] == self.email and item['key'] == self.key]

                return self.filtered

            except KeyError:
                return []

        def get_activity():
            """
            Used to get a specific activity and return it
            :return: specific_activity
            """
            try:
                self.filtered = [item for item in DB['activities'] if item['user'] == self.email and
                                 item['key'] == self.key and
                                 item['activity_key'] == self.activity_key]

                return self.filtered

            except KeyError:
                return []

        if self.bucket:
            return get_bucket()

        if self.activity:
            return get_activity()

    # *********************************

    # *** ACCESSOR METHODS *****

    @staticmethod
    def create_data(*args, **kwargs):
        data = AbstractFeatures(*args, **kwargs)
        return data._create_data()

    @staticmethod
    def read_data(*args, **kwargs):
        data = AbstractFeatures(*args, **kwargs)
        return data._read_data()

    @staticmethod
    def update_data(*args, **kwargs):
        data = AbstractFeatures(*args, **kwargs)
        return data._update_data()

    @staticmethod
    def delete_data(*args, **kwargs):
        data = AbstractFeatures(*args, **kwargs)
        return data._delete_data()

    @staticmethod
    def get_specific_data(*args, **kwargs):
        data = AbstractFeatures(*args, **kwargs)
        return data._get_specific_data()


class CreateBucket(AbstractFeatures, View):
    """
    This function is
    """

    methods = ['GET', 'POST']

    def dispatch_request(self):
        """
        This method is called with all
        the arguments from the URL rule.
        """

        def get():
            if 'user' in session.keys() and 'user' in session.keys() is not None:
                return render_template('create_bucket.html', page='Create Bucket', data=CATEGORIES)
            else:
                return redirect('/login/')

        def post():
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

            else:
                return make_response(jsonify({'error': self.error_message}), 500)

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

            else:
                return make_response(jsonify({'error': self.error_message}), 500)

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
