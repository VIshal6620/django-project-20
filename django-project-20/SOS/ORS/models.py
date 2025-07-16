from django.db import models


class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    loginId = models.EmailField()
    password = models.CharField(max_length=20)
    confirmPassword = models.CharField(max_length=20,default='')
    dob = models.DateField(max_length=20)
    address = models.CharField(max_length=50, default='')
    gender = models.CharField(max_length=50, default='')
    mobileNumber = models.CharField(max_length=50, default='')
    roleId = models.IntegerField()
    roleName = models.CharField(max_length=50)

    def get_key(self):
        return self.id

    def get_value(self):
        return self.firstName + '' + self.lastName

    class Meta:
        db_table = 'sos_user'


class Role(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.name

    class Meta:
        db_table = 'sos_role'

class Position(models.Model):
    designation = models.CharField(max_length=50)
    openingDate = models.DateField(max_length=15)
    requiredExperience = models.CharField(max_length=20)
    condition = models.CharField(max_length=50)

    def get_key(self):
        return str(self.id)

    def get_value(self):
        return self.condition

    class Meta:
        db_table = 'sos_position'

