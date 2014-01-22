from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('app_list', 'api/app-list')
    config.add_route('form_view', 'api/add-app')
    config.add_route('get_list', 'api/pending-list')
    config.add_route('new_app', 'api/new-app')
    config.scan()
    return config.make_wsgi_app()
