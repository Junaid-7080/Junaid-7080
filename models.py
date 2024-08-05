from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Blog(models.Model):
    cat_choice = (("Education","Education"),
                ("Sports","Sports"),
                ("Food","Food"),
                ("Bussiness","Bussiness"),
                ("Movies","Movies"),
                ("Entertainment","Entertainment"),
                ("Technology","Technology"),
                ("Fashion","Fashion"),
                )
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)         
    title = models.CharField(max_length=30,null=True,blank=True)
    content = models.TextField(null=True)
    image = models.ImageField(upload_to='image/',null=True)
    category = models.CharField(max_length=20,choices=cat_choice,default="movies")
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    comment = models.TextField(null=True)
    fk_user = models.ForeignKey(User,on_delete=models.CASCADE)
    fk_blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)


class Userprofile(models.Model):
    gender_choice = (("male","male"),
                     ("female","female"),
                     ("others","others")
    )
    name = models.OneToOneField(User, on_delete=models.CASCADE,max_length=20,related_name='profile')
    address = models.TextField(null=True)
    phonenumber = models.CharField(max_length=10)
    email = models.CharField(null=True,max_length=30)
    gender = models.CharField(choices=gender_choice,default="others",max_length=10)
    image = models.ImageField(upload_to='image/',null=True) 
    dateofbirth = models.DateField()

   
    
class UserOTP(models.Model):
    otp = models.CharField(max_length=5)
    fk_user = models.OneToOneField(User,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now_add=True)


class Sample(models.Model):
    title = models.CharField(max_length=10)
    description = models.TextField()








