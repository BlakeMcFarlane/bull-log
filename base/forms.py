from django import forms

SEMESTER_CHOICES = [
    ('202308',   '2023 | Fall'),
    ('202401', '2024 | Spring'),
    ('202406', '2024 | Summer'),
]

class CourseRegistrationForm(forms.Form):
    semester = forms.CharField(widget=forms.Select(choices=SEMESTER_CHOICES))
    subject = forms.CharField(max_length=10)
    course_number = forms.IntegerField()
