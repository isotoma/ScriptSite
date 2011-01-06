from django.contrib import admin
from scriptsite.main.models import TestScript, TestRun

class TestScriptAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestScript, TestScriptAdmin)

class TestRunAdmin(admin.ModelAdmin):
    pass
admin.site.register(TestRun, TestRunAdmin)