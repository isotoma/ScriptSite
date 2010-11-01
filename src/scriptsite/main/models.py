from django.db import models

class TestScript(models.Model):
    revision = models.CharField(max_length = 15)
    script_file = models.FileField(upload_to='uploaded_scripts/%y%m%d%H%M%S/')
