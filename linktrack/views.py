from requests import get as http_get
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from linktrack.models import Relation, ClickRecord
from django.conf import settings

# http://127.0.0.1:8000/api/track/?e_url=http://127.0.0.1:8000/api/webhook&e_alias=Test&e_email=igor.teplov@actse.ltd&e_email_number=2&e_email_type=B&utm_source=email
@method_decorator([never_cache], name='dispatch')
class TrackView(View):
    def get(self, request, *args, **kwargs):
        custom_code = settings.CUSTOM_CODE
        if f'{custom_code}_url' not in request.GET.keys() or f'{custom_code}_alias' not in request.GET.keys() or f'{custom_code}_email' not in request.GET.keys():
            raise Http404()
        _alias = request.GET[f'{custom_code}_alias']
        _url_for_redirect = request.GET[f'{custom_code}_url']
        _email = request.GET[f'{custom_code}_email']
        relation = get_object_or_404(Relation, alias=_alias)

        # relation.track_all_clicks if False
        # Трекает каждую ссылку с каждого письма по 1 разу, до тех пор пока трек не сочтется успешным
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
            response = http_get(relation.webhook_url, json={
                'email': request.GET[f'{custom_code}_email']
            })

            record = ClickRecord(alias=_alias, url_for_redirect=_url_for_redirect, email=_email, status_code=response.status_code, 
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
