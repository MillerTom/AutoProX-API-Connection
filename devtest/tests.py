import unittest
from pyramid import testing
from suds.client import Client
import settings
import json
import datetime


def register_routes(config):
    config.add_route('home', '/')
    config.add_route('app_list', 'api/app-list')
    config.add_route('form_view', 'api/add-app')
    config.add_route('get_list', 'api/pending-list')
    config.add_route('new_app', 'api/new-app')


def default(obj):
    """JSON serializer for datetime instances"""

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    return obj.ctime()

client = Client(settings.URL)
auth_token = client.service.AuthenticateUser(
    settings.USERNAME,
    settings.PASSWORD,
    settings.API_KEY
)


class HomeViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def call_fut(self, request):
        from devtest.views import home
        return home(request)

    def test_it(self):
        register_routes(self.config)
        request = testing.DummyRequest()
        info = self.call_fut(request)
        self.assertTrue(info['project_name'], 'AutoProX API Connection Demo')


class FormViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def call_fut(self, request):
        from devtest.views import form_view
        return form_view(request)

    def test_it(self):
        register_routes(self.config)
        request = testing.DummyRequest()
        info = self.call_fut(request)
        self.assertTrue(info['title'], 'New Application')


class AppListViewTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def call_fut(self, request):
        from devtest.views import app_list_view
        return app_list_view(request)

    def test_it(self):
        register_routes(self.config)
        request = testing.DummyRequest()
        info = self.call_fut(request)
        self.assertTrue(info['title'], 'AutoProX API')


class AppListRequestTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def call_fut(self, request):
        from devtest.views import get_list
        return get_list(request)

    def test_it(self):
        register_routes(self.config)
        request = testing.DummyRequest()
        info = self.call_fut(request)
        apps = client.service.GetPendingApplicationCertifications(auth_token, True)
        apps = apps.PendingApplicationCertificationsList.PendingApplicationCertifications
        apps_object_list = []
        for i in apps:
            keys = i.__keylist__
            values = []
            for j in keys:
                values.append(i[j])
            apps_object_list.append(dict(zip(keys, values)))

        apps_object_list.sort()
        match = json.dumps(apps_object_list, default=default)
        self.assertEqual(info.body, match)


class NewAppAuthTest(unittest.TestCase):
    """ Negative Test """
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        req = client.service.RequestApplicationNotListed()
        self.assertEqual(u'User Not Authenticated', req.errordescription)


class NewAppTest(unittest.TestCase):
    """ Negative Test """
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_it(self):
        req = client.service.RequestApplicationNotListed(auth_token)
        self.assertEqual(u'ApplicationName cannot be NULL', req.errordescription)
