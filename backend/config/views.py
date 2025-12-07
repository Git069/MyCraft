from django.http import JsonResponse

def api_root(request):
    """
    A simple API root view that provides information about the available endpoints.
    """
    return JsonResponse({
        'message': 'Welcome to the MyCraft API!',
        'endpoints': {
            'admin': '/admin/',
            'auth': '/api/auth/',
            'jobs': '/api/jobs/'
        }
    })
