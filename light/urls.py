from django.urls import path
from light import views

app_name = 'light'

urlpatterns = [
path('', views.index, name='index'),
path('about/', views.about, name='about'),

path('register/', views.register, name = 'register'),
path('login/', views.user_login, name ='login'),
path('error/', views.error, name='error'),
path('logout/', views.user_logout, name='logout'),

path('questionnaire/', views.questionnaire, name = 'questionnaire'),
path('plan/', views.plan, name = 'plan'),
path('update_plan/', views.update_plan, name = 'update_plan'),

path('post/', views.post_challenge, name = "post_challenge"),
path('delete/', views.delete_challenge, name ="delete"),
path('challenges', views.view_challenge, name = "view_challenge"),
path('details/', views.challenge_details, name = 'details'),
path('join/', views.join_challenge, name = 'join'),
path('leave/', views.leave_challenge, name='leave'),
path('update_step_1/', views.update_step_1, name = 'step_1'),
path('update_step_2/', views.update_step_2, name = 'step_2'),
path('update_step_3/', views.update_step_3, name = 'step_3'),

# this path accepts a 'theme' parameter as a String from from the template before redirecting it to the view, enabling theme switching
path('theme/', views.theme, name='theme'),
]
