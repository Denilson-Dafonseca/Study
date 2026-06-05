from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class LearningProfile(models.Model):
    LEARNING_STYLES = [
        ('visual', 'Visual Learner'),
        ('auditory', 'Auditory Learner'),
        ('reading', 'Reading/Writing Learner'),
        ('kinesthetic', 'Kinesthetic Learner'),
        ('mixed', 'Mixed/Combination'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    CONCENTRATION_LEVELS = [
        ('low', 'Low (20-30 min)'),
        ('medium', 'Medium (45-60 min)'),
        ('high', 'High (90+ min)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learning_profile')
    learning_style = models.CharField(max_length=20, choices=LEARNING_STYLES)
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    concentration_level = models.CharField(max_length=20, choices=CONCENTRATION_LEVELS)
    subjects_studying = models.TextField(help_text="Comma-separated list of subjects")
    academic_goals = models.TextField()
    study_challenges = models.TextField()
    available_hours_per_day = models.FloatField(default=2.0)
    preferred_study_times = models.CharField(max_length=100, default="Evening")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Learning Profile"
    
    def get_subjects_list(self):
        return [s.strip() for s in self.subjects_studying.split(',')]

class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_plans')
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    generated_plan = models.TextField()
    weekly_schedule = models.TextField(blank=True, null=True)
    study_techniques = models.TextField(blank=True, null=True)
    revision_schedule = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.subject} Study Plan for {self.user.username}"

class StudySession(models.Model):
    SESSION_TYPES = [
        ('study', 'Study Session'),
        ('revision', 'Revision'),
        ('practice', 'Practice Test'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    study_plan = models.ForeignKey(StudyPlan, on_delete=models.CASCADE, related_name='sessions', null=True, blank=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
    subject = models.CharField(max_length=100)
    duration_minutes = models.IntegerField()
    scheduled_date = models.DateField()
    start_time = models.TimeField()
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.scheduled_date}"

class LearningTip(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    learning_style = models.CharField(max_length=50, blank=True, null=True)
    subject = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField(default=timezone.now)
    total_study_minutes = models.IntegerField(default=0)
    sessions_completed = models.IntegerField(default=0)
    goals_achieved = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date}"