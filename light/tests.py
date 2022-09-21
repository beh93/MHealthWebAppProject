from asyncio.windows_events import NULL
import os
import re
import inspect
import tempfile
from venv import create
import light.models
from light import forms
from populate_light import populate
from django.db import models
from django.test import TestCase
from django.conf import settings
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from django.forms import fields as django_fields
from light.models import Category, Action, UserProfile

#Helper methods
def add_action(action):
    a = Action.objects.get_or_create(prompt=action['prompt'], parent = action['parent'])
    return a

class ObjectCreationTests(TestCase):
    #This series of tests verifies that objects can be created
  
    #1   
    def test_category_creation(self):
        c = Category.objects.get_or_create(name='Test')

        self.assertEqual(c == NULL, False) #if the assertion was True, it would mean that no Category object had been created

    #2
    def test_action_creation(self):
        Category.objects.get_or_create(name='Test')
        c = Category.objects.get(name='Test')

        actions =[{'prompt': 'test',
        'parent': c}]

        for action in actions:
            a = add_action(action)

        action = Action.objects.get(prompt='test') 

        self.assertEqual(action == NULL, False) 

    #3
    def test_userprofile_creation(self):
        User.objects.create_user(username='test', email='test@test.com', password='test123456789@!')
        user = User.objects.get(username='test')

        p = UserProfile.objects.get_or_create(user=user, nickname='test')
        profile = UserProfile.objects.get(user=user)

        #checks that a UserProfile Object was created
        self.assertFalse(profile == NULL)
        #checks that the default theme was correctly loaded
        self.assertTrue(profile.theme == 'sunset')

    #5
    
    
class ProjectConfigurationTests(TestCase):
    #This tests whether templates, static files and media files have been correctly configured to avoid pathing issues later

    
    def setUp(self):
        self.project_base_dir = os.getcwd()
        self.templates_dir = os.path.join(self.project_base_dir, 'templates')
        self.light_templates_dir = os.path.join(self.templates_dir, 'light')

        self.project_base_dir = os.getcwd()
        self.static_dir = os.path.join(self.project_base_dir, 'static')
        self.media_dir = os.path.join(self.project_base_dir, 'media')

    #4   
    def test_template_pathing(self):
        exists = 'TEMPLATE_DIR' in dir(settings)
        self.assertTrue(exists)
        
        template_directory = os.path.normpath(settings.TEMPLATE_DIR)
        soft_template_directory = os.path.normpath(self.templates_dir)
        self.assertEqual(template_directory, soft_template_directory)
        
    #5
    def test_static_directories(self):
        static_directory = os.path.isdir(self.static_dir)
        images_sub = os.path.isdir(os.path.join(self.static_dir, 'images'))
        
        self.assertTrue(static_directory, f"the static directory does not exist.")
        self.assertTrue(images_sub, f"the images subdirectory does not exist")
        

class RegistrationFormTests(TestCase):
    #These tests confirm that the registration forms work correctly

    #6
    def test_correct_user_form(self):
        self.assertTrue('UserForm' in dir(forms), f"The UserForm form does not exist in the forms module")
        
        user_form = forms.UserForm()
        fields = user_form.fields
        
        expected_fields = {
            'username': django_fields.CharField,
            'email': django_fields.EmailField,
            'password': django_fields.CharField,
        }
        
        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{expected_field_name} is not a field in the UserForm.")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{expected_field_name} in UserForm is of the incorrect type.")
    
    #7
    def test_correct_user_profile_form(self):
        self.assertTrue('UserProfileForm' in dir(forms), f"The UserProfileForm cannot be found in the form module")
        
        profile_form = forms.UserProfileForm()
        fields = profile_form.fields

        expected_fields = {
            'nickname': django_fields.CharField,
          }

        for expected_field_name in expected_fields:
            expected_field = expected_fields[expected_field_name]

            self.assertTrue(expected_field_name in fields.keys(), f"{expected_field_name} is not a field in the UserForm.")
            self.assertEqual(expected_field, type(fields[expected_field_name]), f"{expected_field_name} in UserForm is of the incorrect type.")


class UserAuthenticationTests(TestCase):
    #This series of tests checks that the views are operating correctly

    #8    
    def test_registration_get_response(self):
        request = self.client.get(reverse('light:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<h1>Register</h1>' in content, f"find the '<h1>Register for Rango</h1>' header tag in your register template. Did you follow the specification in the book to the letter?")
        self.assertTrue('enctype="multipart/form-data"' in content, f"er.html template, are you using 'multipart/form-data' for the <form>'s 'enctype'?")
        self.assertTrue('action="/light/register/"' in content, f"rm> in register.html pointing to the correct URL for registering a user?")
        self.assertTrue('<input type="submit" name="submit" value="Register" />' in content, f" couldn't find the markup for the form submission button in register.html. Check it matches what is in the book, and try again.")

    #9
    def test_forms_created_successfully(self):
        user_data = {'username': 'testuser', 'password': 'test123', 'email': 'test@test.com'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'nickname': 'tester'}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"The UserForm data is not valid. ")
        self.assertTrue(user_profile_form.is_valid(), f"The ProfileForm data is not valid.")

        user = user_form.save()
        user.set_password(user_data['password'])
        user.save()
        
        profile = user_profile_form.save(commit=False)
        profile.user = user
        profile.save()
        
        self.assertFalse(user == NULL, f"User is null, meaning the object was not created.")
        self.assertFalse(profile == NULL, f"Profile is null, meaning the object was not created.")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"Unable to log in.")
        
    #10
    def test_login_is_working_correctly(self):
        User.objects.create_user(username='test', email='test@test.com', password='test123456789@!')
        user = User.objects.get(username='test')

        response = self.client.post(reverse('light:login'), {'username': 'test', 'password': 'test123456789@!'})
        
        try:
            self.assertEqual(user.id, int(self.client.session['_auth_user_id']), f"Current user was logged in rather than the intended user.")
        except KeyError:
            self.assertTrue(False, f"The login view is not working correctly.")
    #11
    def test_logout_nonuser(self):
        response = self.client.get(reverse('light:logout'))
        self.assertTrue(response.status_code, 302)
        self.assertTrue(response.url, reverse('light:login'))
    #12
    def test_user_logout_working_correctly(self):
        User.objects.create_user(username='test', email='test@test.com', password='test123456789@!')
        user = User.objects.get(username='test')
        self.client.login(username='test', password='test123456789@!')

        try:
            self.assertEqual(user.id, int(self.client.session['_auth_user_id']), f"Current user was logged in rather than the intended user.")
        except KeyError:
            self.assertTrue(False, f"The login view is not working correctly.")

        response = self.client.get(reverse('light:logout'))
        self.assertEqual(response.url, reverse('light:index'), f"Logging out does not redirect users to the index page.")
        self.assertTrue('_auth_user_id' not in self.client.session, f"The user is not logged out. Check the logout view.")
    
    #13
    def test_visible_links_when_logged_in(self):
        User.objects.create_user(username='test', email='test@test.com', password='test123456789@!')
        user = User.objects.get(username='test')

        self.client.login(username='test', password='test123456789@!')
        content = self.client.get(reverse('light:index')).content.decode()
  
        self.assertTrue('href="/light/plan/"' in content, f"se check the links in your base.html have been updated correctly to change when users log in and out.")     

        self.assertTrue('href="/light/login/"' not in content, f"eck the links in your base.html have been updated correctly to change when users log in and out.")
        self.assertTrue('href="/light/register/"' not in content, f"heck the links in your base.html have been updated correctly to change when users log in and out.")
