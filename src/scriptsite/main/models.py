from django.db import models

class TestScript(models.Model):
    script_file = models.FileField(upload_to='/uploaded_scripts/%y%m%d/')
