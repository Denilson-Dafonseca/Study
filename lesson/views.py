from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.db import models  # Add this import
from .forms import UserRegistrationForm, LearningProfileForm
from .models import LearningProfile, StudyPlan, StudySession, UserProgress
from .ai_assistant import WeStudyAI
import json
from datetime import datetime, timedelta

def index(request):
    """Homepage view"""
    return render(request, 'index.html')

def about(request):
    """About page with app information"""
    return render(request, 'about.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your learning profile.')
            return redirect('assessment')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def assessment(request):
    """Learning assessment questionnaire"""
    # Check if user already has a profile
    try:
        profile = request.user.learning_profile
        messages.info(request, 'You already have a learning profile. You can update it or generate a new study plan.')
        return redirect('dashboard')
    except LearningProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = LearningProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            
            # Generate initial study plan using AI
            ai_assistant = WeStudyAI(profile)
            study_plan_data = ai_assistant.generate_study_plan()
            
            # Save the study plan
            for subject in profile.get_subjects_list():
                plan = StudyPlan.objects.create(
                    user=request.user,
                    title=f"{subject} Study Plan",
                    subject=subject,
                    generated_plan=json.dumps(study_plan_data),
                    weekly_schedule=json.dumps(study_plan_data['weekly_schedule']),
                    study_techniques='\n'.join(study_plan_data['study_techniques']),
                    revision_schedule=json.dumps(study_plan_data['revision_plan'])
                )
                
                # Create initial study sessions for the week
                create_initial_sessions(request.user, plan, study_plan_data)
            
            messages.success(request, 'Your learning profile has been created! Your personalized study plan is ready.')
            return redirect('dashboard')
    else:
        form = LearningProfileForm()
    
    return render(request, 'assessment.html', {'form': form})

def create_initial_sessions(user, study_plan, plan_data):
    """Create initial study sessions based on the weekly schedule"""
    today = datetime.now().date()
    
    # Get days of week mapping
    days_map = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day_name, schedule in plan_data['weekly_schedule'].items():
        if day_name in days_map:
            # Find the date for this day of the week
            day_num = days_map.index(day_name)
            days_ahead = (day_num - today.weekday()) % 7
            session_date = today + timedelta(days=days_ahead)
            
            for idx, subject in enumerate(schedule.get('subjects', [])):
                # Create morning sessions (9 AM, 11 AM, etc.)
                start_hour = 9 + idx * 2
                if start_hour < 24:
                    start_time = datetime.strptime(f"{start_hour}:00", "%H:%M").time()
                    
                    StudySession.objects.create(
                        user=user,
                        study_plan=study_plan,
                        session_type='study',
                        subject=subject,
                        duration_minutes=plan_data.get('session_duration', 45),
                        scheduled_date=session_date,
                        start_time=start_time
                    )

@login_required
def dashboard(request):
    """User dashboard showing study progress and plans"""
    try:
        profile = request.user.learning_profile
    except LearningProfile.DoesNotExist:
        return redirect('assessment')
    
    study_plans = StudyPlan.objects.filter(user=request.user, is_active=True)
    upcoming_sessions = StudySession.objects.filter(
        user=request.user,
        scheduled_date__gte=timezone.now().date(),
        completed=False
    ).order_by('scheduled_date', 'start_time')[:10]
    
    recent_sessions = StudySession.objects.filter(
        user=request.user,
        completed=True
    ).order_by('-scheduled_date')[:5]
    
    # Calculate statistics
    total_study_time = StudySession.objects.filter(
        user=request.user,
        completed=True
    ).aggregate(total=models.Sum('duration_minutes'))['total'] or 0
    
    completion_rate = 0
    total_sessions = StudySession.objects.filter(user=request.user).count()
    completed_sessions = StudySession.objects.filter(user=request.user, completed=True).count()
    if total_sessions > 0:
        completion_rate = (completed_sessions / total_sessions) * 100
    
    context = {
        'profile': profile,
        'study_plans': study_plans,
        'upcoming_sessions': upcoming_sessions,
        'recent_sessions': recent_sessions,
        'total_study_time': total_study_time,
        'completion_rate': round(completion_rate, 1)
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def study_plan_detail(request, plan_id):
    """View detailed study plan"""
    study_plan = get_object_or_404(StudyPlan, id=plan_id, user=request.user)
    sessions = StudySession.objects.filter(study_plan=study_plan).order_by('scheduled_date')
    
    # Parse JSON data
    plan_data = {}
    if study_plan.generated_plan:
        try:
            plan_data = json.loads(study_plan.generated_plan)
        except:
            plan_data = {}
    
    context = {
        'study_plan': study_plan,
        'sessions': sessions,
        'plan_data': plan_data
    }
    
    return render(request, 'study_plan.html', context)

@login_required
def custom_logout(request):
    """Custom logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('index')

@login_required
def update_session_status(request, session_id):
    """AJAX endpoint to update study session completion status"""
    if request.method == 'POST':
        session = get_object_or_404(StudySession, id=session_id, user=request.user)
        session.completed = True
        session.status = 'completed'
        session.save()
        
        # Update user progress
        today = timezone.now().date()
        progress, created = UserProgress.objects.get_or_create(
            user=request.user,
            date=today
        )
        progress.total_study_minutes += session.duration_minutes
        progress.sessions_completed += 1
        progress.save()
        
        return JsonResponse({'success': True, 'message': 'Session marked as completed!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'})