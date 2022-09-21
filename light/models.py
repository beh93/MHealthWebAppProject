from django.db import models
from django.contrib.auth.models import User


MAX_LENGTH = 128


#User Models
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nickname = models.CharField(max_length = MAX_LENGTH)
    theme = models.CharField(max_length = MAX_LENGTH, default = 'sunset')

    def __str__(self):
        return self.nickname

#Plan Models
class Category(models.Model):    
    name = models.CharField(max_length = MAX_LENGTH)

    class Meta:
         verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

#This model is responsible for generating the prompts/coping strategies that populate the Plan feature
class Action(models.Model):
    prompt = models.CharField(max_length = MAX_LENGTH)
    parent = models.ForeignKey(Category, on_delete = models.CASCADE)   

    def __str__(self):
        return self.prompt

class Resource(models.Model):
    name = models.CharField(max_length = MAX_LENGTH)
    picture = models.ImageField(upload_to='resource_images', blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return self.name

#This model allows individual steps in the user Plan to be marked complete
class UserPlan(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    action_id = models.ForeignKey(Action, on_delete = models.CASCADE)
    complete = models.BooleanField(default = False)

    def __str__(self):
        return self.user_id.username



#Questionnaire Models
class UserInterests(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    interests = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.username



#Challenge Models
class Challenge(models.Model):
    title = models.CharField(max_length=MAX_LENGTH, unique=True)
    description = models.TextField(max_length = 500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Step_1(models.Model):
    challenge = models.ForeignKey(Challenge, blank = True, on_delete = models.CASCADE)
    text = models.CharField(max_length = MAX_LENGTH)

    def __str__(self):
        return self.text

class Step_2(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete = models.CASCADE)
    text = models.CharField(max_length = MAX_LENGTH, blank = True)

    def __str__(self):
        return self.text

class Step_3(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete = models.CASCADE)
    text = models.CharField(max_length = MAX_LENGTH, blank = True)

    def __str__(self):
        return self.text

class User_Step_1(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    Step_1_id = models.ForeignKey(Step_1, on_delete = models.CASCADE)
    complete = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user_id.username

class User_Step_2(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    Step_2_id = models.ForeignKey(Step_2, on_delete = models.CASCADE)
    complete = models.BooleanField(default = False)

    def __str__(self):
        return self.user_id.username

class User_Step_3(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    Step_3_id = models.ForeignKey(Step_3, on_delete = models.CASCADE)
    complete = models.BooleanField(default = False)
    
    def __str__(self):
        return self.user_id.username

