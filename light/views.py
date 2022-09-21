from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import redirect
from .models import Challenge, Step_1, Step_2, Step_3, User_Step_1, User_Step_2, User_Step_3, UserInterests, Action, UserPlan, Resource, UserProfile
from .forms import UserForm, InterestForm, UserProfileForm, ChallengeForm, ChallengeForm_Step_1, ChallengeForm_Step_2, ChallengeForm_Step_3

#User Views
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        #Ensuring forms are valid prior to saving them in order to create new User and UserProfile objects
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()


            user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password'])
                                
            login(request, user) #logging in users automatically
            return redirect(reverse('light:questionnaire'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'light/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        #Using Django's in-built authentication function to ensure that the username and password are valid
        user = authenticate(username=username, password=password)

        #User is logged in if their details are valid
        if user:
            login(request, user)
            return redirect(reverse('light:plan'))
        #They are redirected to an error message if details are invalid
        else:
            return redirect(reverse('light:error'))
    else:
        return render(request, 'light/login.html')

def error(request):
    return render(request, 'light/error.html')


#Logging out can only be performed if the user is already logged in
@login_required
def user_logout(request):
    #Django's in-built logout function
    logout(request)
    return redirect(reverse('light:index'))
        


#Site Views     
def index(request):
    return render(request, 'light/index.html')


def questionnaire(request):
    #The interest questionnaire which lists all Categories currently stored in the database
    form = InterestForm()
  
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = InterestForm(request.POST)
            
            #Creates a UserInterest obejct if the submitted form is valid
            if form.is_valid():
                questionnaire = form.save(commit = False)
                questionnaire.user = request.user
                questionnaire.save()
                form.save_m2m()

                #Querying database for Actions that belong to the Categories stored in the user's UserInterest model
                interests = UserInterests.objects.filter(user = request.user).values_list('interests')
                action = Action.objects.filter(parent__in = interests)
                current_user = request.user
                
                #Creating a UserPlan based off of all Actions returned by the query above
                for a in action:
                    UserPlan.objects.get_or_create(user_id = current_user, action_id = a)

                return redirect(reverse('light:plan'))
            else:
                print(form.errors)
    
    return render(request, 'light/questionnaire.html', {'form': form})


def about(request):
    return render(request, 'light/about.html')



# Displays the Plan
def plan(request):
    
    #Filtering by user to make sure the correct plan is displayed to the user
    action_list = UserPlan.objects.filter(user_id = request.user)

    resource_list = Resource.objects.all()

    context_dict = {}
    context_dict['actions'] = action_list
    context_dict['resources'] = resource_list

    return render(request, 'light/plan.html', context = context_dict)


def update_plan(request):

    #The id number of the UserPlan object is passed here via URL
    step = request.GET.get('step') #parsing the id
    current_step = UserPlan.objects.get(id = step)#fetching the UserPlan matching the id number from the database
    
    current_step.complete = True  #setting the UserPlan retrieved above as complete
    current_step.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) #redirecting to the same page as the was previously on



#Challenge Views
def view_challenge(request):

    challenges = Challenge.objects.all()

    context = {'challenges' : challenges}

    return render(request, 'light/view_challenge.html', context)


def post_challenge(request):

    #Creating a Challenge requires submission of 4 forms
    if request.method == 'POST':
        challenge_form = ChallengeForm(request.POST)
        first_step_form = ChallengeForm_Step_1 (request.POST)
        second_step_form = ChallengeForm_Step_2(request.POST)
        third_step_form = ChallengeForm_Step_3(request.POST)

        if challenge_form.is_valid() and first_step_form.is_valid() and second_step_form.is_valid() and third_step_form.is_valid():
            #Creating a Challenge object
            challenge = challenge_form.save(commit=False)
            challenge.owner = request.user
            challenge.save()
            
            #Creating the associated first step of the Challenge
            step_1 = first_step_form.save(commit=False)
            step_1.challenge = challenge
            step_1.save()

            #Creating the associated second step of the Challenge
            step_2 = second_step_form.save(commit=False)
            step_2.challenge = challenge
            step_2.save()

            #Creating the associated third step of the Challenge
            step_3 = third_step_form.save(commit=False)
            step_3.challenge = challenge
            step_3.save()

            return redirect(reverse('light:view_challenge'))

        else:
            print(challenge_form.errors, first_step_form.errors, second_step_form.errors, third_step_form.errors)
    else:
        challenge_form = ChallengeForm()
        first_step_form = ChallengeForm_Step_1()
        second_step_form = ChallengeForm_Step_2()
        third_step_form = ChallengeForm_Step_3()
    
    return render(request, 'light/post_challenge.html', context={'challenge_form': challenge_form, 'first_step': first_step_form, 'second_step' : second_step_form, 'third_step': third_step_form})


def delete_challenge(request):
    
    #The title of the Challenge is passed here via url
    title = request.GET.get('title') #Parsing the title

    challenge = Challenge.objects.get(title = title) #retrieving the correct object
    challenge.delete() #deleting the object

    return redirect(reverse('light:view_challenge'))


def challenge_details(request):
    name = request.GET.get('title') #The title of the Challenge is passed here via url
    n_Challenge = Challenge.objects.get(title=name)#retrieving the correct object
    
    user = request.user

    step_1 = Step_1.objects.get(challenge = n_Challenge)
    step_2 = Step_2.objects.get(challenge = n_Challenge)
    step_3 = Step_3.objects.get(challenge = n_Challenge)

    #Logic for displaying which step each user is currently undertaking; broken, needs to be re-engineerd in future work
    try:
        step_1_users = User_Step_1.objects.filter(Step_1_id = step_1)
    except User_Step_1.DoesNotExist:
        print('does not exist')
    try:
        step_2_users = User_Step_2.objects.filter(Step_2_id = step_2)
    except User_Step_2.DoesNotExist:
        print('does not exist')
    try:
        step_3_users = User_Step_3.objects.filter(Step_3_id = step_3)
    except User_Step_3.DoesNotExist:
        print('does not exist')  
    
    context_dict = {}
    context_dict['first_step'] = step_1
    context_dict['second_step'] = step_2
    context_dict['third_step'] = step_3
    context_dict['challenge'] = n_Challenge
    context_dict['current_user'] = user  
    context_dict['step_1_users'] =  step_1_users
    context_dict['step_2_users'] =  step_2_users
    context_dict['step_3_users'] =  step_3_users
     

    return render(request, 'light/challenge_details.html', context=context_dict)


def join_challenge(request):
    name = request.GET.get('title')

    n_Challenge = Challenge.objects.get(title=name)

    step_1 = Step_1.objects.get(challenge = n_Challenge)
    step_2 = Step_2.objects.get(challenge = n_Challenge)
    step_3 = Step_3.objects.get(challenge = n_Challenge)

    # Creating the necessary User_Step_# objects that will allow users to mark individual Challenge steps as complete
    user_step_1 = User_Step_1.objects.get_or_create(user_id = request.user, Step_1_id = step_1)
    user_step_2 = User_Step_2.objects.get_or_create(user_id = request.user, Step_2_id = step_2) 
    user_step_3 = User_Step_3.objects.get_or_create(user_id = request.user, Step_3_id = step_3)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def leave_challenge(request):
    name = request.GET.get('title')

    nChallenge = Challenge.objects.get(title=name)
    user = request.user

    #Deleting all User_Step_# objects associated with the current user and the Challenge they want to leave
    step_1 = Step_1.objects.get(challenge=nChallenge)
    user_step_1 = User_Step_1.objects.get(user_id=user, Step_1_id = step_1)
    user_step_1.delete()

    step_2 = Step_2.objects.get(challenge=nChallenge)
    user_step_2 = User_Step_2.objects.get(user_id=user, Step_2_id = step_2)
    user_step_2.delete()

    step_3 = Step_3.objects.get(challenge=nChallenge)
    user_step_3 = User_Step_3.objects.get(user_id=user, Step_3_id = step_3)
    user_step_3.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_step_1(request):
    step = request.GET.get('step')

    current_step = Step_1.objects.get(id = step)

    #The correct plan step is retrieved by filtering for the correct Challenge using the 'step' variable received from the front end via URL
    update_step = User_Step_1.objects.get(Step_1_id = current_step, user_id = request.user)

    #Marking the relevant User_Step_1 object as complete 
    update_step.complete = True
    update_step.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_step_2(request):
    step = request.GET.get('step')

    current_step = Step_2.objects.get(id = step)

    update_step = User_Step_2.objects.get(Step_2_id = current_step, user_id = request.user)

    #Marking the relevant User_Step_2 object as complete 
    update_step.complete = True
    update_step.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def update_step_3(request):
    step = request.GET.get('step')

    current_step = Step_3.objects.get(id = step)

    update_step = User_Step_3.objects.get(Step_3_id = current_step, user_id = request.user)

    #Marking the relevant User_Step_3 object as complete 
    update_step.complete = True
    update_step.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



# Theme-Switching View
def theme(request):
    theme = request.GET.get('theme')
    user_theme = UserProfile.objects.get(user = request.user) #Retrieving the current user's UserProfile object, which stores theme
    user_theme.user = request.user
    
    user_theme.theme = theme #Changing the stores theme to the theme passed from the front end
    user_theme.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
