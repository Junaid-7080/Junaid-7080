from django.shortcuts import render,redirect
from django.http import HttpResponse
from . models import Blog,Comment,Userprofile,UserOTP,Sample
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .form import BlogForm,SampleFrom
import random
from django.core.mail import send_mail
from django.views.generic import ListView,CreateView,UpdateView,DetailView,ListView
from django.urls import reverse_lazy,reverse

# Create your views here.

def sample(request):
    return HttpResponse('welcome to kerala')

def junaid(request):
    return HttpResponse('codeme')


def demo(request):
    return render(request,"demo.html")




def codeme(request):
    return render(request,"codeme.html")


def dynamic(request):
    context = {'name': 'jhon'}
    return render(request,"dynamic.html",context)

def names(request):
    context = {'name':[ 'jhon','anu','aravindh']}
    return render(request,"loop.html",context)


def dict(request):
    data = [
        {"name":'junaid','age':'22','place':'malappuram'},
        {"name":'aswanth','age':'21','place':'vadakara'},
        {"name":'rajeer','age':'24','place':'kannur'},
    ]
    context ={ "students": data }
    return render(request,"dict.html",context)

@login_required(login_url="login")
def home(request):
    blog = Blog.objects.filter(is_published=True)
    if request.method == "POST":
        search = request.POST.get("search")
        blog = Blog.objects.filter(title__icontains = search)
    context = {'blog':blog}
    return render(request,"home.html",context)


@login_required(login_url="login")
def blog_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")
        cate = request.POST.get('cate')
        blog = Blog.objects.create(title=title,content=content,image=image,category=cate,fk_user=request.user)
        blog.save()
        messages.success(request,'Blog created successfully...')
        return redirect('home')
    messages.error(request,'Blog creation failed...')
    context = {'cat':Blog.cat_choice}
    return render(request,'blog_create.html',context)

@login_required(login_url="login")
def blog_detail(request,blog_id):
    try:
        blog_obj =Blog.objects.get(id = blog_id)
    except:
        blog_obj=None
    if request.method == 'POST':
        comment = request.POST.get('comment')
        Comment.objects.create(comment = comment,fk_user =request.user,fk_blog = blog_obj)
        messages.success(request,'commenet posted successfully.....')
    messages.error(request,'comment posted failed......')

    comments = Comment.objects.filter(fk_blog=blog_obj)
    context = {'blog':blog_obj,'comments':comments}
    return render(request,"blog_detail.html",context)


@login_required(login_url="login")
def blog_edit(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog=None
    if request.user != blog.fk_user:
        return HttpResponse('sorry,permission Denied')
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        cate = request.FILES.get('cate')
        if title:      
            blog.title=title
        if content:
            blog.content=content
        if image:
            blog.image=image
        if cate:
            blog.category=cate
        blog.fk_user=request.user
        blog.save()
        messages.success(request,"Registration successfully!")
        return redirect('detail',blog.id)
    messages.error(request,"password dosen't match.. please try again...")
    
    context = {'blog':blog,'cat':Blog.cat_choice}
    return render(request,"blog_edit.html",context)


@login_required(login_url="login")
def blog_delete(request,id):
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog = None
    if request.user != blog.fk_user:
        return HttpResponse('sorry,permission Denied')
    if request.method =='POST':
        blog.delete()
        messages.success(request,'Blog deleted successfully...')
        return redirect('home')
    messages.error(request,'Blog deletion failed....')
    context = {'blog':blog}
    return render(request,'blog_delete.html',context)


def register(request):
    if request.method=='POST':
        username = request.POST.get('username') 
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
           user=User.objects.create_user(username=username,email=email,password=password1)
           user.save()
           messages.success(request,"Registration successfully!")
           return redirect('login')
        messages.error(request,"password dosen't match.. please try again...")
    return render(request,'register.html')


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if  user.is_superuser:
                messages.success(request, "login successfully..")
                return redirect('admin_home')
            elif Userprofile.objects.filter(name = user).exists():
                return redirect('home')
            else:
                messages.success(request,"login successfully")
                return redirect('user_create')
        messages.error(request,"User does n't exist...please register...")
        return redirect('register')
    return render(request,'user_login.html')


def user_logout(request):
    logout(request)
    messages.success(request,'successfully logout...')
    return redirect('login')

@login_required(login_url="login")
def comment_edit(request,id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        comment=None
    if request.user != blog.fk_user:
        return HttpResponse('sorry,permission Denied')
    blog = comment.fk_blog
    comments =Comment.objects.filter(fk_blog=blog)
    if request.method == "POST":
        edited_comment=request.POST.get('comment')
        comment.comment=edited_comment
        comment.save()
        return redirect('detail',blog.id)
    context = {'comment':comment,'blog':blog,'comments':comments}
    return render(request,'blog_detail.html',context)


@login_required(login_url="login")
def comment_delete(request,id):
    try:
        comment = Comment.objects.get(id=id)
    except:
        comment = None
    if request.user != comment.fk_user:
        return HttpResponse('sorry,permission Denied')
    comment.delete()
    return redirect('detail',comment.fk_blog.id) 


def user_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phonenumber = request.POST.get('phonenumber')
        email = request.POST.get('email')
        gen = request.POST.get('gender')
        print('gen',gen)
        image = request.FILES.get('image')
        dateofbirth = request.POST.get('dateofbirth')
        userprofile = Userprofile.objects.create(name=request.user,address=address,phonenumber=phonenumber,email=email,gender=gen,image=image,dateofbirth=dateofbirth)
        userprofile.save()
        return redirect('home')
    return render(request,'user_profile.html')


def user_detail(request,user_id):
    profile = get_object_or_404(User,id=user_id)
    context = {'profile':profile}
    return render(request,'user_profile_detail.html',context)



    

@login_required(login_url="login")
def admin_home(request):
    if not request.user.is_superuser:
        return HttpResponse('permission Denied')
    try:
        blog = Blog.objects.all()
    except:
        blog =None

    context ={'blog':blog}
    return render(request,'admin_home.html',context)



@login_required(login_url="login")
def change_status(request,id):
    if not request.user.is_superuser:
        return HttpResponse('permission Denied')
    try:
        blog = Blog.objects.get(id=id)
    except:
        blog = None
    blog.is_published = not blog.is_published
    blog.save()
    messages.success(request,'status changed!')
    return redirect('admin_home')

def user_home_get(request):
    return render(request,'user_home_get.html')


def create_new(request):
    form = BlogForm()
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.fk_user = request.user
            blog.save()
            messages.success(request,'Blog created successfully')
            return redirect("home")
        messages.error(request,form.errors)
    context = {'form':form}
    return render(request,'create_new.html',context)

def blog_edit_new(request,id):
    blog = Blog.objects.get(id=id)
    form = BlogForm(instance=blog)
    if request.method == "POST":
        form = BlogForm(request.POST,request.FILES,instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.fk_user = request.user
            blog.save()
            messages.success(request,'Blog Updated successfully')
            return redirect("detail",id)
        messages.error(request,form.errors)
    context = {'form':form}
    return render(request,'blog_edit_new.html',context)


def forgot(request):
    if request.method == "POST":
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            otp = random.randrange(1000,9999)
            email = user.email
            print(email)
            subject = "OTP verification"
            message = f"This is your One Time password {otp}"
            from_email = "junaidabdrahiman15@gmail.com"
            to = [email]
            send_mail(
                subject = subject,
                message = message,
                from_email = from_email,
                recipient_list = to,
                fail_silently = False 
            )
            UserOTP.objects.update_or_create(fk_user=user,defaults={'otp':otp})
            messages.success(request,"OTP send successfully")
            return redirect('otp_verify',user.id)
        message.error(request,'User not found!,please register')
        return redirect('register')
    return render(request,'forgot.html')

def otp_verify(request,id):
    user = User.objects.filter(id=id).first()
    user_obj = UserOTP.objects.filter(fk_user=user).first()
    send_otp =user_obj.otp
    if request.method == 'POST':
        submitted_otp = request.POST.get('otp')
        if submitted_otp == send_otp:
            messages.success(request,'Otp verified successfully! ')
            return redirect('password_reset',id)
        messages.error(request,'OTP verification failed! please try again...')
    return render(request,'otp_verify.html')

def password_reset(request,id):
    user = User.objects.filter(id=id).first()
    if request.method =='POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            user.set_password(password2)
            user.save()
            messages.success(request,'password Reste Successfully')
            return redirect('login')
        messages.error(request,'password mismatch,please reenter !')
    return render(request,'password_reset.html')



class SampleCreate(CreateView):
    model = Sample
    template_name = 'junaid.html'
    form_class = SampleFrom
    success_url = reverse_lazy('home')

class SampleUpdate(UpdateView):
    model = Sample
    template_name = 'junaid_edit.html'
    form_class = SampleFrom
    success_url = reverse_lazy('sam_detail')
    def get_success_url(self):
        return reverse('sam_detail', kwargs={'pk': self.object.pk})

class SampleList(ListView):
    model = Sample
    template_name = 'sample_home.html'
    context_object_name = 'sam_obj'

class SampleDetail(DetailView):
    model = Sample
    template_name = 'sample_detail.html'
    context_object_name = 'sam'


def vitez(request):
    return render(request,'vitez.html')