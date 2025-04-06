from django.db import models
from django.conf import settings
import os

class Resume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='resumes/%Y/%m/%d/', null=True, blank=True)
    content = models.TextField(blank=True)
    skills = models.JSONField(default=dict)
    experience = models.JSONField(default=list)
    education = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def delete(self, *args, **kwargs):
        # Delete the file when the resume is deleted
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)

class ResumeAnalysis(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='analyses')
    ats_score = models.FloatField()
    ats_details = models.JSONField(default=dict)
    skills_match = models.JSONField(default=dict)
    missing_skills = models.JSONField(default=dict)
    improvement_suggestions = models.JSONField(default=dict)
    format_analysis = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Analysis for {self.resume.title}"
