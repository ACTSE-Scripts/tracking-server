from requests import get as http_get
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import HttpResponsePermanentRedirect, Http404

from linktrack.models import Relation, ClickRecord

# http://127.0.0.1:8000/api/track/?url=https://google.com&alias=Test&email=igor.teplov@actse.ltd&email_number=2&email_type=B
class TrackView(View):
    def get(self, request, *args, **kwargs):
        if 'url' not in request.GET.keys() or 'alias' not in request.GET.keys() or 'email' not in request.GET.keys():
            raise Http404()
        _alias = request.GET['alias']
        _url_for_redirect = request.GET['url']
        _email = request.GET['email']
        relation = get_object_or_404(Relation, alias=_alias)
        response = http_get(relation.webhook_url, json={
            'email': request.GET['email']
        })
        record = ClickRecord(alias=_alias, url_for_redirect=_url_for_redirect, email=_email, status_code=response.status_code, 
            email_number=request.GET.get('email_number', 1), email_type=request.GET.get('email_type', 'A'))
        record.save()
        return HttpResponsePermanentRedirect(_url_for_redirect)
