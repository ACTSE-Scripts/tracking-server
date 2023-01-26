from django.contrib import admin
from linktrack.models import Relation, ClickRecord

@admin.register(Relation)
class RelationAdmin(admin.ModelAdmin):
    pass

@admin.register(ClickRecord)
class ClickRecordAdmin(admin.ModelAdmin):
    list_filter = ('alias',)
    search_fields = ('alias', 'email', 'url_for_redirect')
