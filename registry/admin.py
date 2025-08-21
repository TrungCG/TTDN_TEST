from django.contrib import admin

from .models import CommuneCurrent, CommuneOld, Merger, District, Province

admin.site.register(CommuneCurrent)
admin.site.register(CommuneOld)
admin.site.register(Merger)
# admin.site.register(CommuneAlias)
admin.site.register(District)
admin.site.register(Province)

