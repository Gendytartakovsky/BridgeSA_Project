from django.db import models
from django.contrib.auth.models import User

# Extend default user (optional extras)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username


# Core model for BridgeSA
class DocumentSubmission(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    document = models.FileField(upload_to='uploads/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    # Optional — could later be used for printable packs
    reference_code = models.CharField(max_length=12, unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"
