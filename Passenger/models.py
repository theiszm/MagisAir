from django.db import models

from django.contrib.auth.models import User

class Passenger(models.Model):
    """ A user model for passenger. """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, 
        choices=[('F', 'Female'), ('M', 'Male')], 
        default='', null=True, blank=True, 
    )
    
    def __str__(self):
        middle_initial = f"{self.middle_name[0]}." if self.middle_name else ""
        return f"{self.last_name}, {self.first_name} {middle_initial}".strip()
    
    def __str__(self):
        middle_initial = f"{self.middle_name[0]}." if self.middle_name else ""
        return f"{self.last_name}, {self.first_name} {middle_initial}".strip()
    
    def get_absolute_url(self):
        return reverse('passenger', args=[self.pk])
