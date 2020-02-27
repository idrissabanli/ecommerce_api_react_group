from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users', blank=True, null=True)

    def get_user_avatar(self):
        if self.image:
            return self.image
        else:
            return 'https://img.favpng.com/8/19/8/united-states-avatar-organization-information-png-favpng-J9DvUE98TmbHSUqsmAgu3FpGw.jpg'
