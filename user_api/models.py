import uuid
from django.db import models


class UserModel(models.Model):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid1, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=13, unique=True)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=1, default='M')

    def __str__(self):
        return 'User Model\nName: {}\nEmail: {}\nAge: {}\nGender:\n'.\
            format(self.name, self.email, self.age, self.gender)
