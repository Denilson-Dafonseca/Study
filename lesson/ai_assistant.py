import random
import json
from datetime import datetime, timedelta

class WeStudyAI:
    """AI-powered study assistant that generates personalized study strategies"""
    
    def __init__(self, learning_profile):
        self.profile = learning_profile
        self.learning_style = learning_profile.learning_style
        self.difficulty = learning_profile.difficulty_level
        self.concentration = learning_profile.concentration_level
        self.subjects = learning_profile.get_subjects_list()
        
    def generate_study_plan(self):
        """Generate a complete personalized study plan"""
        
        # Calculate optimal session duration based on concentration level
        session_duration = self._get_session_duration()
        
        # Get appropriate study techniques for learning style
        techniques = self._get_study_techniques()
        
        # Generate weekly schedule
        weekly_schedule = self._generate_weekly_schedule(session_duration)
        
        # Generate revision strategy
        revision_plan = self._generate_revision_plan()
        
        # Create memory techniques
        memory_techniques = self._get_memory_techniques()
        
        plan = {
            'summary': self._generate_plan_summary(),
            'session_duration': session_duration,
            'daily_hours': self.profile.available_hours_per_day,
            'study_techniques': techniques,
            'weekly_schedule': weekly_schedule,
            'revision_plan': revision_plan,
            'memory_techniques': memory_techniques,
            'subject_priority': self._prioritize_subjects(),
            'tips_for_success': self._get_success_tips()
        }
        
        return plan
    
    def _get_session_duration(self):
        """Determine optimal study session duration based on concentration level"""
        durations = {
            'low': 25,  # Pomodoro-style
            'medium': 45,
            'high': 60
        }
        return durations.get(self.concentration, 45)
    
    def _get_study_techniques(self):
        """Return study techniques tailored to learning style"""
        techniques = {
            'visual': [
                "Create mind maps and diagrams for complex topics",
                "Use color-coded notes and highlighters",
                "Watch educational videos and animations",
                "Create flashcards with images",
                "Use visual analogies to remember concepts"
            ],
            'auditory': [
                "Record yourself reading notes and listen back",
                "Study in groups and discuss topics aloud",
                "Use mnemonic devices and rhymes",
                "Listen to educational podcasts",
                "Explain concepts to others verbally"
            ],
            'reading': [
                "Write detailed summaries of each topic",
                "Create outlines and bullet-point notes",
                "Read textbooks actively with highlighting",
                "Rewrite important information in your own words",
                "Create comparison charts and tables"
            ],
            'kinesthetic': [
                "Take frequent movement breaks",
                "Use hands-on experiments and activities",
                "Walk while reciting information",
                "Build physical models or use manipulatives",
                "Act out historical events or scientific processes"
            ],
            'mixed': [
                "Combine multiple techniques for each study session",
                "Rotate between visual, auditory, and hands-on activities",
                "Create multimedia study materials",
                "Use different methods for different subjects",
                "Test which techniques work best for each topic"
            ]
        }
        
        techniques_list = techniques.get(self.learning_style, techniques['mixed'])
        
        # Add difficulty-specific advice
        if self.difficulty == 'beginner':
            techniques_list.append("Start with basic concepts before moving to complex material")
            techniques_list.append("Use plenty of examples and practice problems")
        elif self.difficulty == 'advanced':
            techniques_list.append("Focus on connecting concepts across subjects")
            techniques_list.append("Teach difficult concepts to others to deepen understanding")
            
        return techniques_list
    
    def _generate_weekly_schedule(self, session_duration):
        """Generate a weekly study schedule based on available time"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_schedule = {}
        
        # Calculate number of sessions per day
        hours_available = self.profile.available_hours_per_day
        sessions_per_day = int(hours_available * 60 / session_duration)
        
        # Adjust for weekends if less time available
        for day in days:
            is_weekend = day in ['Saturday', 'Sunday']
            sessions = max(1, sessions_per_day - 1 if is_weekend else sessions_per_day)
            
            # Distribute subjects throughout the week
            daily_subjects = self._distribute_subjects(day, sessions)
            
            schedule_entry = {
                'sessions': sessions,
                'subjects': daily_subjects,
                'total_minutes': sessions * session_duration,
                'break_suggestion': self._get_break_suggestion(session_duration)
            }
            weekly_schedule[day] = schedule_entry
            
        return weekly_schedule
    
    def _distribute_subjects(self, day, num_sessions):
        """Distribute subjects across sessions for a given day"""
        if not self.subjects:
            return ["General Study"] * num_sessions
            
        # Rotate subjects and prioritize difficult ones earlier in the week
        subject_priority = self._prioritize_subjects()
        daily_subjects = []
        
        # Morning sessions for difficult subjects
        difficult_subjects = [s for s in subject_priority if subject_priority[s] == 'high']
        easy_subjects = [s for s in subject_priority if subject_priority[s] == 'low']
        
        for i in range(num_sessions):
            if i < len(difficult_subjects):
                daily_subjects.append(difficult_subjects[i % len(difficult_subjects)])
            else:
                daily_subjects.append(random.choice(easy_subjects if easy_subjects else self.subjects))
                
        return daily_subjects
    
    def _prioritize_subjects(self):
        """Prioritize subjects based on difficulty and goals"""
        priority = {}
        for subject in self.subjects:
            # In a real implementation, this would use actual performance data
            # For now, random but realistic prioritization
            if 'math' in subject.lower() or 'science' in subject.lower():
                priority[subject] = 'high'
            elif 'language' in subject.lower():
                priority[subject] = 'medium'
            else:
                priority[subject] = 'low'
        return priority
    
    def _generate_revision_plan(self):
        """Create a spaced repetition revision schedule"""
        revision_intervals = {
            '1_day': 1,
            '3_days': 3,
            '1_week': 7,
            '2_weeks': 14,
            '1_month': 30
        }
        
        return {
            'method': 'Spaced Repetition System',
            'intervals': revision_intervals,
            'instructions': [
                "Review new material within 24 hours of learning it",
                "Second review after 3 days",
                "Third review after 1 week",
                "Fourth review after 2 weeks",
                "Final review after 1 month for long-term retention",
                "Use active recall - test yourself without looking at notes"
            ],
            'weekly_revision_tips': [
                "Dedicate Sundays for weekly revision",
                "Mix old and new topics during revision sessions",
                "Create summary sheets for quick review"
            ]
        }
    
    def _get_memory_techniques(self):
        """Provide memory enhancement techniques"""
        techniques = [
            {
                'name': 'Active Recall',
                'description': 'Test yourself instead of just re-reading notes',
                'implementation': 'After studying, close your book and write down everything you remember'
            },
            {
                'name': 'Spaced Repetition',
                'description': 'Review information at increasing intervals',
                'implementation': 'Use flashcards with a spaced repetition system'
            },
            {
                'name': 'Mnemonics',
                'description': 'Create memory aids like acronyms or rhymes',
                'implementation': 'Create memorable phrases where the first letter of each word represents key information'
            },
            {
                'name': 'Chunking',
                'description': 'Break large amounts of information into smaller groups',
                'implementation': 'Group related concepts together and master one chunk at a time'
            },
            {
                'name': 'Story Method',
                'description': 'Connect information through a narrative',
                'implementation': 'Create a story that links all the key points you need to remember'
            }
        ]
        
        # Add learning style specific memory techniques
        if self.learning_style == 'visual':
            techniques.append({
                'name': 'Memory Palace',
                'description': 'Associate information with locations in an imagined space',
                'implementation': 'Place visual representations of information along a familiar route'
            })
        elif self.learning_style == 'auditory':
            techniques.append({
                'name': 'Rhythm and Rhyme',
                'description': 'Put information to music or rhythm',
                'implementation': 'Create songs or rhymes to remember sequences or lists'
            })
            
        return techniques
    
    def _generate_plan_summary(self):
        """Generate a personalized summary of the study plan"""
        summaries = [
            f"Based on your {self.learning_style} learning style and {self.concentration} concentration level, "
            f"you'll study best in {self._get_session_duration()}-minute focused sessions with regular breaks.",
            
            f"Your personalized plan prioritizes understanding over memorization, using "
            f"{self.learning_style}-specific techniques to maximize retention.",
            
            f"With {self.profile.available_hours_per_day} hours available daily, you can make significant progress "
            f"by following this structured approach to studying."
        ]
        return " ".join(summaries)
    
    def _get_break_suggestion(self, session_duration):
        """Suggest appropriate break times"""
        if session_duration <= 25:
            return "Take a 5-minute break between sessions"
        elif session_duration <= 45:
            return "Take a 10-minute break between sessions"
        else:
            return "Take a 5-minute break every 25 minutes, and a longer 15-minute break after 2 sessions"
    
    def _get_success_tips(self):
        """Provide additional tips for study success"""
        tips = [
            "Create a dedicated study space free from distractions",
            "Turn off phone notifications during study sessions",
            "Stay hydrated and keep healthy snacks nearby",
            "Get adequate sleep - it's crucial for memory consolidation",
            "Review difficult material at different times of the day",
            "Teach concepts to someone else to reinforce understanding",
            "Set specific, measurable goals for each study session",
            "Reward yourself after completing study goals"
        ]
        
        # Add concentration-specific tips
        if self.concentration == 'low':
            tips.extend([
                "Use the Pomodoro Technique (25 minutes study, 5 minutes break)",
                "Start with shorter sessions and gradually increase duration",
                "Remove all potential distractions before starting"
            ])
        elif self.concentration == 'high':
            tips.extend([
                "Take advantage of your long attention span for deep work",
                "Use longer sessions to tackle complex topics",
                "Remember to still take breaks to prevent burnout"
            ])
            
        return tips