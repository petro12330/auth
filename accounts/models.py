from django.db import models
from uuid import uuid4


class User(models.Model):
    ROLE = [
        ('None', 'user'),
        ('a', 'admin'),

    ]
    uuid = models.UUIDField(primary_key=True, default=uuid4)

    login = models.CharField(max_length=200, unique=True, verbose_name='login')
    password = models.CharField(max_length=200, verbose_name='password')
    is_archive = models.BooleanField(default=True)
    role = models.CharField(max_length=255, verbose_name='Role', choices=ROLE)

    def __str__(self):
        return self.login

    class Meta:
        db_table = 'Users'
