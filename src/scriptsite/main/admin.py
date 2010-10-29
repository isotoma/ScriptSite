from django.contrib import admin
from scriptsite.main.models import TestScript

class TestScriptAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestScript, TestScriptAdmin)