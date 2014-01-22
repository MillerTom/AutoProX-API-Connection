from pyramid.view import view_config
from pyramid.response import Response
from devtest.api import AutoProx
import devtest.settings

api = AutoProx(
    devtest.settings.USERNAME,
    devtest.settings.PASSWORD,
    devtest.settings.API_KEY,
    devtest.settings.URL
)

@view_config(route_name='home', renderer='templates/api_home.pt')
def home(request):
    return {'project_name': 'AutoProX API Connection Demo'}


@view_config(route_name='app_list', renderer='templates/app_list.pt')
def app_list_view(request):
    return {'title': 'AutoProX API'}


@view_config(route_name='form_view', renderer='templates/add_app.pt')
def form_view(request):
    return {'title': 'New Application'}


@view_config(route_name='get_list')
def get_list(request):
    """
    Initializes the API connection and returns pending applications' list.
    """
    # TODO: Pagination for long results

    return Response(api.get_pending_apps())


@view_config(route_name='new_app')
def new_application(request):
    """
    When an application posted, forwards the request to the API module,
    If request was successful renders the message from API.
    """
    # TODO: Ajax requests

    res = api.add_new_application(request)
    if res:
        return Response(res)
    else:
        return Response('Error')
