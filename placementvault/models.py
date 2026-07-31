from django.contrib.auth.models import User
from django.db import models


class Schedule(models.Model):
    """An upcoming interview a student wants to keep track of."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedules')
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    interview_round = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.company_name} \u2014 {self.role} on {self.date}"


class Experience(models.Model):
    """An interview experience a student publishes after a placement round."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    interview_round = models.CharField(max_length=150)
    focus_subject = models.CharField(max_length=150)
    experience_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.company_name} \u2014 {self.role} \u2014 {self.interview_round}"
