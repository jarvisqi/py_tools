from django.db import models


# Create your models here.

class Dreamreal(models.Model):
    website = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    phone_number = models.IntegerField()
<<<<<<< HEAD:webapp/djangoapp/models.py
    # online = models.ForeignKey('Online')
=======
    online = models.ForeignKey('Online',on_delete=models.CASCADE)
>>>>>>> d9d8d8e3fb3504dcfecc95466b907cc913e29ab9:djangoweb/web/models.py

    # 表面
    class Meta:
        db_table = "dreamreal"


class Online(models.Model):
    domain = models.CharField(max_length=50)

    class Meta:
        db_table = "online"
