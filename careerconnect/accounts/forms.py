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
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update(
                {'class': 'custom-input'}
            )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # These fields must match the names in models.py
        fields = ['headline', 'skills', 'education', 'work_experience', 'linkedin_link', 'portfolio_link', 'is_public']

        # This adds the styling and placeholders directly to the form
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'custom-input', 'placeholder': 'e.g. Software Engineer'}),
            'skills': forms.Textarea(attrs={'class': 'custom-input', 'rows': 4, 'placeholder': 'Python, Django...'}),
            'education': forms.Textarea(attrs={'class': 'custom-input', 'rows': 4}),
            'work_experience': forms.Textarea(attrs={'class': 'custom-input', 'rows': 5}),
            'linkedin_link': forms.URLInput(attrs={'class': 'custom-input'}),
            'portfolio_link': forms.URLInput(attrs={'class': 'custom-input'}),
        }
