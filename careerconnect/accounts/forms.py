from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import Profile



class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    is_recruiter = forms.BooleanField(
        required=False,
        label="I am a Recruiter",
        help_text="Check this box if you are a recruiter"
    )
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'custom-input'}
            )
        self.fields['is_recruiter'].widget.attrs.update({'class': 'custom-checkbox'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address', 'city', 'state', 'headline', 'skills', 'education', 'work_experience', 'linkedin_link', 'portfolio_link', 'is_public']

        widgets = {
            'address': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'e.g. 123 Main St (optional)'}),
            'city': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'e.g. Atlanta'}),
            'state': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'e.g. GA'}),
            'headline': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'e.g. Software Engineer'}),
            'skills': forms.Textarea(attrs={'class': 'custom-input', 'rows': 4, 'placeholder': 'Python, Django...'}),
            'education': forms.Textarea(attrs={'class': 'custom-input', 'rows': 4}),
            'work_experience': forms.Textarea(attrs={'class': 'custom-input', 'rows': 5}),
            'linkedin_link': forms.URLInput(attrs={'class': 'custom-input'}),
            'portfolio_link': forms.URLInput(attrs={'class': 'custom-input'}),
        }
