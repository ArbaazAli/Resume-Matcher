from django.db import models

class Jd(models.Model):
    name = models.CharField(max_length=20)
    jd = models.FileField(upload_to='jd/')

    def __str__(self):
        return self.name