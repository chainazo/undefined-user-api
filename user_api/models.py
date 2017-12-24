from django.db import models


class UserModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)

    def __str__(self):
        return 'User Model\nName: {}\nEmail: {}\nAge: {}\nGender:\n'.\
            format(self.name, self.email, self.age, self.gender)
