from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from django import forms
from .models import Profile
from django.contrib.auth.models import User



class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([
            f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    is_recruiter = forms.BooleanField(
        required=False,
        label="I am a Recruiter",
        help_text="Check this box if you are a recruiter"
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name', 'is_recruiter')
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'is_recruiter':
                field.widget.attrs.update({'style': 'width: 20px; height: 20px; cursor: pointer; flex-shrink: 0;'})
            else:
                field.widget.attrs.update({'class': 'custom-input'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


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
