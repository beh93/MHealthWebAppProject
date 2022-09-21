import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'light_project.settings')

import django
django.setup()
from light.models import Action, Category, Challenge, Step_1, Step_2, Step_3, Resource, User

def populate():
    cats = {'Anxiety',
        'Fitness',
        'Health',
        'Productivity',
        'Sleep'}
    
    # Adding Categories using data from the cats dictionary to populate the table
    for c in cats:
        add_cat(c)

    productivity = Category.objects.get(name='Productivity')

    actions = [
        {'prompt': 'For the next 3 days, do not snooze your alarm',
        'parent': productivity},
        {'prompt': 'Start setting your alarm 30 minutes earlier than you usually would',
        'parent': productivity},
        {'prompt': 'After getting out of bed, do one quick chore that you have been putting off',
        'parent': productivity},
        {'prompt': 'Take 5 minutes each morning to write a quick to-do list for the day',
        'parent': productivity},
        {'prompt': 'From the beginning of next week, find 10 minutes to write a to-do list of the major things you want to achieve this week',
        'parent': productivity},
        {'prompt': 'Take a big task you have been trying to complete and, on a piece of paper, break it down into a series of smaller tasks',
        'parent': productivity},
        {'prompt': 'Give yourself a reward for finishing a task you have been meaning to finish',
        'parent': productivity},
        ]

    # Adding Actions using data from the actions dictionary
    for action in actions:
        add_action(action)

    
    resources =[
        {'name': 'How to Stop Snoozing your Alarm',
        'link': 'https://www.fastcompany.com/3061222/8-strategies-to-help-you-quit-the-snooze-button-habit-for-',
        'picture': '/light/static/images/resource/alarm.jpg'},
        {'name': 'Tips for Becoming an Morning Bird',
        'link': 'https://www.herzing.edu/blog/8-genius-tips-waking-early',
        'picture': '/static/images/resource/early.jpg'},
        {'name': 'How to Find Time for Daily Chores',
        'link': 'https://lifehacker.com/how-to-find-more-time-in-your-day-by-putting-your-chore-5829673',
        'picture': '/light/static/images/resource/housework.jpg'},
        {'name': 'Creating Amazing and Effective To-Do Lists',
        'link': 'https://www.lifehack.org/articles/productivity/how-to-create-a-to-do-list-that-makes-you-smile.html',
        'picture': '/light/static/images/resource/to_do.jpg'},
        {'name': 'How to Tackle Overwhelming Projects',
        'link': 'https://medium.com/better-with-purpose/how-to-tackle-large-overwhelming-projects-at-home-or-work-982de17bc660',
        'picture': '/light/static/images/resource/milestone.jpg'},
        {'name': 'Building Positive, Lasting Habits',
        'link': 'https://zenhabits.net/sticky/',
        'picture': '/light/static/images/resource/habits.jpg'}
    ]

    # Adding resources 
    for resource in resources:
        add_resource(resource) 

    # Creating a user to act as the Challenge owner 
    User.objects.create_user(username='population_test', email='test@test.com', password='testing1234@!')
    user = User.objects.get(username='population_test')

    challenges =[
        {'title': 'Happy Mornings',
        'description': 'This challenge is meant to get you productive bright and early to make you feel like you have made the absolute most of your morning!',
        'owner': user},
        {'title': 'Be a weekend warrior!',
        'description': 'If you are anything like me, weekdays are a no-go for actually getting out of the house on a run because I am too busy with work and the kids and doing all the household chores the hubby absolutely cannot do haha So why not make the most of our weekends instead to get those miles in! Walk, run, swim, whatever, just do it a lot on the weekend! Whos with me?',
        'owner': user},
    ]

    # Adding Challenges
    for challenge in challenges:
        add_challenge(challenge) 

    # Filtering the database for some challenges to populate with tasks
    morning = Challenge.objects.get(title='Happy Mornings')
    weekend = Challenge.objects.get(title='Be a weekend warrior!')

    step_1 = [
        {'challenge': morning,
        'step': 'For the next week, set your alarm 30 minutes earlier than you normally would'},
        {'challenge': weekend,
        'step': 'Wake up at 8 a.m. on Saturday morning and go for a 30 minute run! (or swim or hike, whatever floats your boat)'},
    ]

    step_2 = [
        {'challenge': morning,
        'step': 'For the next week, don NOT snooze your alarm'},
        {'challenge': weekend,
        'step': 'Rest is for the weak! On Sat evening, go for a brisk 5 mile walk in an area of your choosing. Bonus if there are hills!'},
    ]

    step_3 = [
        {'challenge': morning,
        'step': 'Each day for the next week, do one small task you have been putting off before breakfast'},
        {'challenge': weekend,
        'step': 'Okay guys. Sunday. Time for one last mega push before the weekend is over! Have a long workout today of at least 2 hours'},
    ]

    # Adding steps to the aforementioned Challenges
    for step in step_1:
        add_step_1(step)

    for step in step_2:
        add_step_2(step) 

    for step in step_3:
        add_step_3(step) 
    
# Helper methods  
def add_cat(name):
    cat = Category.objects.get_or_create(name=name)
    return cat

def add_action(action):
    act = Action.objects.get_or_create(prompt=action['prompt'], parent = action['parent'])
    return act

def add_resource(resource):
    r = Resource.objects.get_or_create(name = resource['name'], link = resource['link'], picture = resource['picture'])
    return r

def add_challenge(challenge):
    chal = Challenge.objects.get_or_create(title=challenge['title'], description=challenge['description'], owner= challenge['owner'])
    return chal

def add_step_1(step):
    st = Step_1.objects.get_or_create(challenge=step['challenge'], text = step['step'])
    return st

def add_step_2(step):
    st = Step_2.objects.get_or_create(challenge = step['challenge'], text = step['step'])
    return st

def add_step_3(step):
    st = Step_3.objects.get_or_create(challenge = step['challenge'], text = step['step'])
    return st

# Execution 
if __name__ == '__main__':
    print('Starting population script...')
    populate()
