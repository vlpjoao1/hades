from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.db import models

# Create your models here.

#Debido a que AbstractUser contiene ya varios campos creados, no necesitamos renombrar campos.
from config.settings import MEDIA_URL, STATIC_URL


class User(AbstractUser):
    image = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        # imagen por defecto si no se ingresó imagen
        return '{}{}'.format(STATIC_URL, 'img/empty.png')