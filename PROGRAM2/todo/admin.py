from django.contrib import admin
from .models import Category, Tag, Todo


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Todo)