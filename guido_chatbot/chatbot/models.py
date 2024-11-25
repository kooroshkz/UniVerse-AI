from django.db import models

class StaffMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)
    news = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
