import cherrypy
import itertools

def json_encode(value):
    response = cherrypy.lib.jsontools.json_encode(value)
    
    # Wrap the json output in the callback function, if it exists
    callback = cherrypy.request.params.get('callback')
    if callback:
        # json_encode returns an iterable, so we must chain it with our own iterables heere
        return itertools.chain((callback.encode('utf-8'), b"("), response, (b");",))
    return response

def callback_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return json_encode(value)
