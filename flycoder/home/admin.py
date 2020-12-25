from django.contrib import admin

# Register your models here.
from .models import Contact,Post,BlogComment
admin.site.register((Contact,BlogComment))
admin.site.register(Post)
