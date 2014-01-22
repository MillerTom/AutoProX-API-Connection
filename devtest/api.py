from suds.client import Client
import json
import datetime


class AutoProx():
    """
    A class for connecting to AutoProx API and calling SOAP Actions.
    API credentials can be changed from setting.py
    """

    def __init__(self, username, password, api_key, url):
        self.username = username
        self.password = password
        self.api_key = api_key
        self.url = url
        try:
            self.client = Client(self.url)
        except:
            raise StandardError

        self.auth_token = self.client.service.AuthenticateUser(
            self.username,
            self.password,
            self.api_key
        )

    def get_pending_apps(self):
        """
        Calls API's GetPendingApplicationCertifications function
        with authorization token and returns the result as JSON.
        GetPendingApplicationCertifications(AuthToken, ShowPendingRequestOnly=Boolean)
        """
        # TODO: Pagination
        apps = self.client.service.GetPendingApplicationCertifications(self.auth_token, True)
        try:
            apps = apps.PendingApplicationCertificationsList.PendingApplicationCertifications
        except AttributeError:
            return "There was a problem, try again later."
        apps_object_list = []
        for i in apps:
            keys = i.__keylist__
            values = []
            for j in keys:
                values.append(i[j])
            apps_object_list.append(dict(zip(keys, values)))

        apps_object_list.sort()
        return json.dumps(apps_object_list, default=self.default)

    def add_new_application(self, request):
        """
        Makes a request to API's RequestApplicationNotListed function to add a new app.
        Returns the result message depending on the answer from server.
        """
        name = request.json_body['ApplicationName']
        version = request.json_body['VersionInformation']
        website = request.json_body['ApplicationWebsite']
        download_link = request.json_body['DownloadLink']
        client_names = request.json_body['ClientNames']
        additional_notes = request.json_body['AdditionalNotes']
        requested_by = request.json_body['RequestedBy']

        req = self.client.service.RequestApplicationNotListed(
            self.auth_token,
            name,
            version,
            website,
            download_link,
            client_names,
            additional_notes,
            requested_by
        )
        if not req.CommandSuccessful:
            return req.errordescription.decode()
        else:
            return "Application sent!"

    @staticmethod
    def default(obj):
        """JSON serializer for datetime instances"""

        if isinstance(obj, datetime.datetime):
            if obj.utcoffset() is not None:
                obj = obj - obj.utcoffset()
        return obj.ctime()
