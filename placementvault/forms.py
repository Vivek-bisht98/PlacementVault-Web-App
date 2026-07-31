from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Experience, Schedule

# Suggested roles for the datalist on Schedule/Experience forms.
# Users can still type any custom role - this is suggestion, not restriction.
ROLE_CHOICES = [
    "Software Engineer",
    "Associate Software Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "Python Developer",
    "Data Analyst",
    "Business Analyst",
    "Data Scientist",
    "ML Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "QA Engineer",
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class _NormalizedTextMixin:
    """
    Strips whitespace and title-cases free-text fields listed in
    normalized_fields, so "infosys", "INFOSYS " and "Infosys" all end up
    as the same string. Without this, the search screen would split one
    company into several near-duplicate branches.
    """
    normalized_fields = []

    def _clean_normalized(self, field_name):
        value = self.cleaned_data.get(field_name, '')
        return value.strip().title()


class ScheduleForm(_NormalizedTextMixin, forms.ModelForm):
    normalized_fields = ['company_name', 'role', 'interview_round']

    class Meta:
        model = Schedule
        fields = ['company_name', 'role', 'interview_round', 'date', 'time']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Infosys'}),
            'role': forms.TextInput(attrs={'list': 'role-options', 'placeholder': 'e.g. Specialist Programmer'}),
            'interview_round': forms.TextInput(attrs={'placeholder': 'e.g. Technical Round'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_company_name(self):
        return self._clean_normalized('company_name')

    def clean_role(self):
        return self._clean_normalized('role')

    def clean_interview_round(self):
        return self._clean_normalized('interview_round')


class ExperienceForm(_NormalizedTextMixin, forms.ModelForm):
    normalized_fields = ['company_name', 'role', 'interview_round', 'focus_subject']

    class Meta:
        model = Experience
        fields = ['company_name', 'role', 'interview_round', 'focus_subject', 'experience_text']
        widgets = {
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Infosys'}),
            'role': forms.TextInput(attrs={'list': 'role-options', 'placeholder': 'e.g. Specialist Programmer'}),
            'interview_round': forms.TextInput(attrs={'placeholder': 'e.g. Technical Round'}),
            'focus_subject': forms.TextInput(attrs={'placeholder': 'e.g. DSA, SQL, DBMS'}),
            'experience_text': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Describe the questions asked, the format, and any tips for future candidates...'}),
        }

    def clean_company_name(self):
        return self._clean_normalized('company_name')

    def clean_role(self):
        return self._clean_normalized('role')

    def clean_interview_round(self):
        return self._clean_normalized('interview_round')

    def clean_focus_subject(self):
        return self._clean_normalized('focus_subject')
