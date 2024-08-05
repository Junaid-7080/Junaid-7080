from django.contrib import admin
from.models import Blog,Comment,Userprofile,UserOTP

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','content','category','created_date','updated_date']
    list_filter = ['title','category']
    search_fields = ['title']



admin.site.register(Blog,BlogAdmin)
admin.site.register(Comment)
admin.site.register(Userprofile)
admin.site.register(UserOTP)


