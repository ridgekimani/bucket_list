import os
import shelve

from flask import request, render_template, Flask, jsonify, make_response, redirect, session

from flask.views import View

from datetime import date

app = Flask(__name__)

SHELVE_DB = 'bucket_list_db'

app.config.from_object(__name__)

db = shelve.open(os.path.join(app.root_path, app.config['SHELVE_DB']), writeback=True)

app.secret_key = 'this is a secret'


@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('registration/register.html')

    if request.method == 'POST':
        data = request.form.to_dict()
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if not username:
            return make_response(jsonify({'error': 'Please enter your username'}), 500)

        if not password:
            return make_response(jsonify({'error': 'Please enter your password'}), 500)

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
        username = data.get('username')
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
    def __init__(self, *args, **kwargs):
        self.details = kwargs
        self.args = args
        self.message = None
        self.error_message = None
        self.username = None
        self.bucket_name = None
        self.description = None
        self.bucket = False
        self.activity = False
        self.filtered = None
        self.initialize()

    def initialize(self):
        map(lambda x: self.details.update(dict(x, )), self.args)
        for key, value in self.details.items():
            setattr(self, key, value)

    def _create_data(self):
        def add_bucket():
            values = dict(user=self.username, bucket_name=self.bucket_name, description=self.description,
                          created=date.today())

            if 'buckets' in db.keys():
                db['buckets'].append(values)
            else:
                db['buckets'] = [values]
            self.message = 'Data created successfully'
            return self

        def add_activity():
            return self

        if self.bucket:
            return add_bucket()

        elif self.activity:
            return add_activity()

    def _read_data(self):
        try:
            self.filtered = [item for item in db['buckets'] if item['user'] == self.username]
            return self.filtered

        except KeyError:
            return False

    def _update_data(self):
        pass

    def _delete_data(self):
        pass

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


class CreateBucket(AbstractFeatures, View):

    methods = ['GET', 'POST']

    def dispatch_request(self):

        def get():
            if 'user' in session.keys() and 'user' in session.keys() is not None:
                return render_template('create_bucket.html', page='Create Bucket')
            else:
                return redirect('/login/')

        def post():
            username = session.get('user')
            data = request.form.to_dict()
            bucket_name = data.get('bucket_name')
            description = data.get('description')
            category = data.get('category')
            data = dict(bucket=True, username=username, bucket_name=bucket_name, category=category,
                        description=description)
            response = self.create_data(**data)
            if response.message:
                return make_response(jsonify({'success': 'Bucket Created successfully'}))

        if request.method == 'GET':
            return get()

        elif request.method == 'POST':
            return post()

        else:
            return get()


class ViewBucket(AbstractFeatures, View):

    methods = ['GET']

    def dispatch_request(self):
        if 'user' in session.keys() and 'user' in session.keys() is not None:
            details = self.read_data(username=session.get('user'), bucket=True)
            if details:
                new_details = {}
                for i, d in enumerate(details):
                    new_details[i] = d
                return render_template('view_bucket.html', details=new_details, data=True, page='View Buckets')
            return render_template('view_bucket.html', data=False, page='View Buckets')
        else:
            return redirect('/login/')


class UpdateBucket(AbstractFeatures, View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        pass


class AddActivities(AbstractFeatures, View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        pass


app.add_url_rule('/create_bucket/', view_func=CreateBucket.as_view('create_bucket'))
app.add_url_rule('/view_buckets/', view_func=ViewBucket.as_view('view_buckets'))
app.add_url_rule('/update_bucket/', view_func=UpdateBucket.as_view('update_bucket'))
app.add_url_rule('/add_activities/', view_func=AddActivities.as_view('add_activities'))
