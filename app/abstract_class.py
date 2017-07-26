"""
This class is used to implement the CRUD operations of buckets and activities
"""
import uuid

from datetime import date

DB = dict()


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
            """
            This method is used to delete the specified bucket
            :return: self
            """
            DB['buckets'] = [item for item in DB['buckets'] if item['key'] != self.key]
            try:

                DB['activities'] = [item for item in DB['activities'] if item['key'] != self.key]
            except KeyError:
                pass

            self.message = 'Bucket deleted successfully'
            return self

        def delete_activity():
            """
            This method is used to delete the specified activity
            :return: self
            """

            DB['activities'] = [item for item in DB['activities']
                                if item['activity_key'] != self.activity_key]

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
        :return: self
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
        """
        Accessor method used create data
        :param args:
        :param kwargs:
        :return: create_data
        """
        data = AbstractFeatures(*args, **kwargs)
        return data._create_data()

    @staticmethod
    def read_data(*args, **kwargs):
        """
        Accessor method used to read data
        :param args:
        :param kwargs:
        :return: read_data
        """
        data = AbstractFeatures(*args, **kwargs)
        return data._read_data()

    @staticmethod
    def update_data(*args, **kwargs):
        """
        Accessor method used to update data
        :param args:
        :param kwargs:
        :return: update_data
        """
        data = AbstractFeatures(*args, **kwargs)
        return data._update_data()

    @staticmethod
    def delete_data(*args, **kwargs):
        """
        Accessor method used to delete specific data
        :param args:
        :param kwargs:
        :return: delete_data
        """
        data = AbstractFeatures(*args, **kwargs)
        return data._delete_data()

    @staticmethod
    def get_specific_data(*args, **kwargs):
        """
        Accessor method used to get specific bucket or activity
        :param args:
        :param kwargs:
        :return: get_specific_data
        """
        data = AbstractFeatures(*args, **kwargs)
        return data._get_specific_data()
