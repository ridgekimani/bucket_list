import uuid

from flask import request, render_template, Flask, jsonify, make_response, redirect, session

from flask.views import View

from datetime import date

app = Flask(__name__)

app.config.from_object(__name__)

app.secret_key = 'this is a secret'

db = dict()

categories = [
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
    return redirect('/login/')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration/register.html')

    if request.method == 'POST':
        data = request.form.to_dict()
        username = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not username:
            return make_response(jsonify({'error': 'Please enter your email'}), 500)

        if len(username) < 5:
            return make_response(jsonify({'error': 'Username too short. Please enter more than 4 characters'}), 500)

        if not password:
            return make_response(jsonify({'error': 'Please enter your password'}), 500)

        if len(password) < 8:
            return make_response(jsonify({'error': 'Please enter more than 8 characters for your password'}), 500)

        if not confirm_password:
            return make_response(jsonify({'error': 'Please confirm your password'}), 500)

        if password != confirm_password:
            return make_response(jsonify({'error': 'Passwords do not match'}), 500)

        if username in db.keys():
            return make_response(jsonify({'error': 'User already exists with that username'}), 500)

        db[username] = password
        session['user'] = username
        return jsonify({'success': 'Account created successfully'})


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('registration/login.html')

    if request.method == 'POST':
        data = request.form.to_dict()
        username = data.get('email')
        password = data.get('password')

        if username not in db.keys():
            return make_response(jsonify({'error': 'Username not found. Please sign up to continue'}), 500)

        for key, value in db.items():
            if key == username:
                if value == password:
                    session['user'] = username
                    return jsonify({'success': 'Authenticated successfully'})
                else:
                    return make_response(jsonify({'error': 'Incorrect password'}), 500)

            else:
                return make_response(jsonify({'error': 'Username not found. Please sign up to continue'}), 500)


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
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
        self.username = None
        self.bucket_name = None
        self.description = None
        self.category = None
        self.bucket = False
        self.activity = False
        self.filtered = None
        self.key = None
        self.activity_key = None
        self.initialize()

    def initialize(self):
        """
        Maps arguments to keyword arguments and assigns the values to the attributes with the same name
        when the __init__ method is called
        :return: dict values
        """
        map(lambda x: self.details.update(dict(x, )), self.args)
        for key, value in self.details.items():
            setattr(self, key, value)

    def _create_data(self):
        """
        This private method is used to create data for both buckets and activities
        This method contains two methods, add_bucket and add_activity and the correct functionality is
        used when specifying if its a bucket or activity as an argument
        :return:
        """
        def add_bucket():
            x = uuid.uuid4()
            key = str(x)[:8]
            values = dict(user=self.username, bucket_name=self.bucket_name, description=self.description,
                          category=self.category, created=date.today(), key=key)

            if 'buckets' in db.keys():
                db['buckets'].append(values)
            else:
                db['buckets'] = [values]
            self.message = 'Data created successfully'
            return self

        def add_activity():
            x = uuid.uuid4()
            key = str(x)[:8]
            values = dict(user=self.username, description=self.description,  created=date.today(),  activity_key=key,
                          key=self.key)

            if 'activities' in db.keys():
                db['activities'].append(values)

            else:
                db['activities'] = [values]

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
            try:
                self.filtered = [item for item in db['buckets'] if item['user'] == self.username]
                return self.filtered

            except KeyError:
                return []

        def read_activities():
            try:
                self.filtered = [item for item in db['activities']
                                 if item['user'] == self.username and item['key'] == self.key]

                x = self.get_specific_data(bucket=True, username=self.username, key=self.key)

                new_details = {}
                for i, d in enumerate(x):
                    new_details[i] = d

                val = ''
                for value in new_details.values():
                    for key, val in value.items():
                        if key == 'bucket_name':
                            break

                self.bucket_name = val
                return self

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
            bucket = [item for item in db['buckets'] if item['key'] == self.key]
            new_details = {}
            for i, d in enumerate(bucket):
                new_details[i] = d

            for values in new_details.values():
                values['bucket_name'] = self.bucket_name
                values['description'] = self.description
                values['category'] = self.category

            self.message = 'Bucket updated successfully'
            return self

        def update_activity():
            activity = [item for item in db['activities']
                        if item['key'] == self.key and item['activity_key'] == self.activity_key]

            print(activity)

        if self.bucket:
            return update_bucket()

        if self.activity:
            return update_activity()

    def _delete_data(self):

        def delete_bucket():
            db['buckets'] = [item for item in db['buckets'] if item['key'] != self.key]
            db['activities'] = [item for item in db['activities'] if item['key'] != self.key]

            self.message = 'Bucket deleted successfully'
            return self

        def delete_activity():
            db['activities'] = [item for item in db['activities']
                                if item['key'] != self.key and item['activity_key'] != self.activity_key]

            self.message = 'Activity successfully deleted'
            return self

        if self.bucket:
            return delete_bucket()

        if self.activity:
            return delete_activity()

    def _get_specific_data(self):
        """
        This method is used to get specific data unit given the key and the username
        It is used while creating a bucket activity or updating the bucket
        :return:
        """
        def get_bucket():
            try:
                self.filtered = [item for item in db['buckets']
                                 if item['user'] == self.username and item['key'] == self.key]

                return self.filtered

            except KeyError:
                return []

        if self.bucket:
            return get_bucket()

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

    methods = ['GET', 'POST']

    def dispatch_request(self):

        def get():
            if 'user' in session.keys() and 'user' in session.keys() is not None:
                return render_template('create_bucket.html', page='Create Bucket', data=categories)
            else:
                return redirect('/login/')

        def post():
            username = session.get('user')
            data = request.form.to_dict()
            bucket_name = data.get('bucket_name')
            description = data.get('description')
            value = data.get('category')
            category = ''

            for category_ in categories:
                for key, val in category_.items():
                    if key == value:
                        category = val

            data = dict(bucket=True, username=username, bucket_name=bucket_name, category=category,
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

    methods = ['GET']

    def dispatch_request(self):
        if 'user' in session.keys() and 'user' in session.keys() is not None:
            details = self.read_data(username=session.get('user'), bucket=True)
            if details:
                new_details = {}
                for i, d in enumerate(details):
                    new_details[i] = d
                return render_template('view_buckets.html', details=new_details, data=True,
                                       page='View Buckets')
            return render_template('view_buckets.html', data=False, page='View Buckets')
        else:
            return redirect('/login/')


class UpdateBucket(AbstractFeatures, View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        def get():
            unique_key = request.args.get('key')

            if not unique_key:
                return redirect('/view_buckets/')

            if 'user' in session.keys() and 'user' in session.keys() is not None:
                data = self.get_specific_data(key=unique_key, username=session.get('user'), bucket=True)
                if data:
                    new_details = {}
                    for i, d in enumerate(data):
                        new_details[i] = d

                    return render_template('update_bucket.html', page='Update Bucket', data=new_details,
                                           categories=categories, unique_key=unique_key)
            else:
                return redirect('/login/')

        def post():
            username = session.get('user')
            data = request.form.to_dict()
            bucket_name = data.get('bucket_name')
            description = data.get('description')
            value = data.get('category')
            unique_key = data.get('key')
            category = ''

            for category_ in categories:
                for key, val in category_.items():
                    if key == value:
                        category = val

            data = dict(bucket=True, username=username, bucket_name=bucket_name, category=category, key=unique_key,
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
    methods = ['POST']

    def dispatch_request(self):
        username = session.get('user')
        data = request.form.to_dict()
        unique_key = data.get('key')
        description = data.get('text')
        if not unique_key:
            return make_response(jsonify({'error': 'Please select a specific bucket'}), 500)

        if not description:
            return make_response(jsonify({'error': 'Please enter your activities'}), 500)

        data = dict(activity=True, username=username, description=description, key=unique_key )

        response = self.create_data(**data)
        if response.message:
            return make_response(jsonify({'success': 'Activity added successfully'}))


class ViewActivities(AbstractFeatures, View):
    methods = ['GET']

    def dispatch_request(self):
        key = request.args.get('key')
        if not key:
            return redirect('/view_buckets/')

        if 'user' in session.keys() and 'user' in session.keys() is not None:
            details = self.read_data(username=session.get('user'), activity=True, key=key)
            if details.filtered:
                new_details = {}
                for i, d in enumerate(details.filtered):
                    new_details[i] = d

                return render_template('view_activities.html', details=new_details, data=True,
                                       page='View Buckets', bucket=details.bucket_name)
            return render_template('view_activities.html', data=False, page='View Buckets')
        else:
            return redirect('/login/')


class UpdateActivity(AbstractFeatures, View):
    methods = ['POST']

    def dispatch_request(self):
        username = session.get('user')
        data = request.form.to_dict()
        key = data.get('bucket_name')
        description = data.get('description')
        activity_key = data.get('key')

        data = dict(activity=True, username=username, key=key, description=description, activity_key=activity_key)

        response = self.update_data(**data)

        if response.message:
            return make_response(jsonify({'success': 'Activity Updated successfully'}), 200)

        else:
            return make_response(jsonify({'error': self.error_message}), 500)


class DeleteData(AbstractFeatures, View):

    methods = ['POST']

    def dispatch_request(self):
        data = request.form.to_dict()
        key = data.get('key')
        bucket = data.get('bucket')
        activity = data.get('activity')
        activity_key = data.get('activity_key')

        if not key:
            return make_response(jsonify({'error': 'Please select a specific bucket or activity'}), 500)

        def delete_bucket():
            values = dict(key=key, bucket=True)
            response = self.delete_data(**values)

            if response.message:
                return make_response(jsonify({'success': 'Bucket deleted successfully'}))

        def delete_activity():
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
