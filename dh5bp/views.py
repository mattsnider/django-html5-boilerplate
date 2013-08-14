from django.views import defaults


def page_not_found(request):
    """Handle the server_error view"""
    return defaults.page_not_found(request, template_name='dh5bp/404.html')


def server_error(request):
    """Handle the server_error view"""
    return defaults.server_error(request, template_name='dh5bp/500.html')