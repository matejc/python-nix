from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid_zodbconn import get_connection
from pyramid import renderers
from .models import appmaker


def root_factory(request):
    conn = get_connection(request)
    return appmaker(conn.root())


def add_cors_headers_response_callback(event):
    def cors_headers(request, response):
        response.headers.update({
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
            'Access-Control-Allow-Headers':
            'Origin, Content-Type, Accept, Authorization',
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Max-Age': '1728000',
        })

    event.request.add_response_callback(cors_headers)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(root_factory=root_factory, settings=settings)

    json_renderer = renderers.JSON()
    config.add_renderer(None, json_renderer)

    config.add_subscriber(add_cors_headers_response_callback, NewRequest)

    config.add_route('api.things.get', '/api/things', request_method='GET')

    config.scan()
    return config.make_wsgi_app()
