from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404


class RedirectAdminToPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if not path.startswith('/admin/') and ('/admin/' in path or path.endswith('/admin')):
            raise Http404()

        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            is_admin_path = path.startswith('/admin/')
            is_logout_path = path.startswith(reverse('admin:logout')) if 'admin' in path else False
            is_media_static = path.startswith('/static/') or path.startswith('/media/')

            if not (is_admin_path or is_logout_path or is_media_static):
                return redirect('/admin/')

        return self.get_response(request)