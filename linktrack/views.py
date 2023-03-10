from requests import get as http_get
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponsePermanentRedirect, Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from linktrack.models import Relation, ClickRecord
from django.conf import settings

@method_decorator([never_cache], name='dispatch')
class TrackView(View):
    def get(self, request, *args, **kwargs):
        custom_code = settings.CUSTOM_CODE
        if f'{custom_code}_url' not in request.GET.keys() or f'{custom_code}_email' not in request.GET.keys():
            raise Http404()
        _alias = kwargs.get('alias', 'test')
        _url_for_redirect = request.GET[f'{custom_code}_url']
        _email = request.GET[f'{custom_code}_email']
        relation = get_object_or_404(Relation, alias=_alias)

        if relation.unique_click_by_link:
            additional_filter = {}
        else:
            additional_filter = {'email_number': request.GET.get(f'{custom_code}_email_number', 1)}
        _track = False
        if relation.track_all_clicks:
            _track = True
        else:
            clicks = ClickRecord.objects.filter(
                alias=_alias, email=_email,
                url_for_redirect=_url_for_redirect, status_code=200, **additional_filter
            ).count()
            if clicks == 0:
                _track = True
        if _track:
            if not any(list(map(lambda host: host in relation.webhook_url, settings.ALLOWED_HOSTS))): 
                response = http_get(relation.webhook_url, json={
                    'email': request.GET[f'{custom_code}_email']
                }).status_code
            else:
                response = 500

            record = ClickRecord(alias=_alias, url_for_redirect=_url_for_redirect, email=_email, status_code=response, 
                email_number=request.GET.get(f'{custom_code}_email_number', 1), email_type=request.GET.get(f'{custom_code}_email_type', 'A'))
            record.save()

        if not _url_for_redirect.endswith('/'):
            _url_for_redirect = _url_for_redirect + '/'

        included_get = []
        for key, value in request.GET.items():
            if key not in [f'{custom_code}_url', f'{custom_code}_email', f'{custom_code}_alias', f'{custom_code}_email_number', f'{custom_code}_email_type']:
                included_get.append(f'{key}={value}')
        _get = ''
        if len(included_get) != 0:
            get_data = '&'.join(included_get)
            _get = f'?{get_data}'
        return HttpResponsePermanentRedirect(f'{_url_for_redirect}{_get}')

class TrackWebhook(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Ok')

@method_decorator([never_cache], name='dispatch')
class UrlBuilder(LoginRequiredMixin, View):
    login_url = '/admin/login/?next=/'
    redirect_field_name = 'next'
    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'alias': Relation.objects.only('alias').values_list('alias')})
