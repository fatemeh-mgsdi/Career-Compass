from django.db import models
from users.models import User
from resumes.models import Resume

class Interview(models.Model):
    INTERVIEW_TYPES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('system_design', 'System Design'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='interviews')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='interviews')
    title = models.CharField(max_length=100)
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES)
    job_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.title}"

class Question(models.Model):
    CATEGORIES = [
        ('technical', 'Technical'),
        ('behavioral', 'Behavioral'),
        ('system_design', 'System Design'),
    ]
    
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    suggested_answer = models.TextField(blank=True)
    key_points = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Question for {self.interview.title}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    audio_file = models.FileField(upload_to='interview_answers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Answer by {self.user.email} for {self.question.text[:50]}..."

class InterviewFeedback(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='feedback')
    clarity_score = models.FloatField()
    technical_score = models.FloatField()
    confidence_score = models.FloatField()
    feedback_text = models.TextField()
    improvement_suggestions = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.answer.user.email}'s answer to {self.answer.question.text[:50]}..."
