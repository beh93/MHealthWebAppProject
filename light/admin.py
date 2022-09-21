from django.contrib import admin
from .models import Category, UserInterests, Resource, Action, Challenge, Step_1, Step_2, Step_3
from django.contrib import admin

admin.site.register(Category)
admin.site.register(Action)
admin.site.register(Resource)
admin.site.register(Challenge)
admin.site.register(Step_1)
admin.site.register(Step_2)
admin.site.register(Step_3)
