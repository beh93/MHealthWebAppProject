from django import forms
from django.contrib.auth.models import User 
from .models import Category, Challenge, Step_1, Step_2, Step_3, UserInterests, UserPlan, UserProfile

#User Forms

#This form is used during registration
class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        
        #setting all field labels to be blank so they can be renamed via helptext
        labels = {
            'username': '', 
            'email': '',
            'password': '',
}

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email-Address'}),
            'password': forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'})
        }

#This form is used during registration, creating the UserProfile model
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('nickname',)
        labels = {'nickname': '',}

        widgets = {
            'nickname': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Public Nickname'})
        }


#Interest Quiz forms

#This generates the interest Questionnaire that users fill out during registration
class InterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset = Category.objects.all(), widget = forms.CheckboxSelectMultiple)

    class Meta:
        model = UserInterests
        fields = ('interests',)


#Challenge forms

#This generates a Challenge
class ChallengeForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ('title', 'description',)

        labels = {
            'title': '', 
            'description': '',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder': 'description'}),
        }

#This generates the first step of a Challenge
class ChallengeForm_Step_1(forms.ModelForm):
    class Meta:
        model = Step_1
        fields = ('text',)

        labels = {
            'text': '', 
        }

        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Step 1'}),
        }

#This generates the second step of a Challenge
class ChallengeForm_Step_2(forms.ModelForm):
    class Meta:
        model = Step_2
        fields = ('text',)

        labels = {
            'text': '', 
        }

        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Step 2'}),
        }

#This generates a third step of the Challenge
class ChallengeForm_Step_3(forms.ModelForm):
    class Meta:
        model = Step_3
        fields = ('text',)

        labels = {
            'text': '', 
        }

        widgets = {
            'text': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Step 3'}),
        }
