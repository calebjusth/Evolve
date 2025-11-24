# jobs/models.py
from django.db import models
from django.urls import reverse

class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200, default="Our Company")
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default='full_time')
    department = models.CharField(max_length=200, blank=True)
    salary_range = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.location}"
    
    def get_absolute_url(self):
        return reverse('job_detail', kwargs={'pk': self.pk})