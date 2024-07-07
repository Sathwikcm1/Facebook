from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User, auth
# from django.http import HttpResponse
from django.contrib import messages
from .models import Profile,Post,LikePost,followersCount
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import logout
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username = request.user.username)        #creating a variable to store the user object, this is used to get the user object.
    user_profile = Profile.objects.get(user = user_object)           # ?we are getting the user profile from the database. using the user object we are getting the user profile.
    
    posts = Post.objects.all()
    posts_profiles = {post: Profile.objects.get(user__username=post.user) for post in posts}  
    return render(request,'index.html', {'user_profile':user_profile,'posts':posts,'posts_profiles': posts_profiles})          #sending the user profile to the index.html page.

@login_required(login_url='signin')
def like_post(request):
    
    
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id = post_id)       #this is to get the post object from the database.
    
    like_filter = LikePost.objects.filter(post_id = post_id, username = username).first() #this is to check if the user has already liked the post or not.
    
    if like_filter is None:  # this means that the user has not liked the post yet.
        new_like = LikePost.objects.create(post_id = post_id,username = username)
        new_like.save()
        post.no_of_likes += 1           #this is to increment the number of likes by one.
        post.save()                         #this is to save the changes to the database.
        return redirect('/')      #this is to redirect the user to the index page.
    else: 
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1;
        post.save()
        return redirect('/')
@login_required(login_url='signin')
def profile(request, pk):                 # so this is the profile page, we are passing the pk which is the user id.
    user_object= User.objects.get(username = pk)
    user_profile = Profile.objects.get(user = user_object)
    user_post = Post.objects.filter(user = pk)                  # pk is basically the username of the user. so in Post model we can see that the user is the user object which is now assigned to the pk.
    user_post_length = len(user_post)
    
    context = {
        'user_profile':user_profile,
        'user_object':user_object,
        'user_posts':user_post,
        'user_post_length':user_post_length,
    }
    return render(request,'profile.html',context)

@login_required(login_url='signin')   
def follow(request):     # this is the follow button to work in the profile.html.
    if request == 'POST':
        follower = request.POST['follower']
        user  = request.POST['user']
    else:
        return redirect('/')

@login_required(login_url='signin')
def upload(request):
    if request.method == "POST":
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        
        new_post = Post.objects.create(user=user,image = image , caption=caption)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    return HttpResponse('<h1> mew</h1>')


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user= request.user)  # we are getting the user profile from the database.
    
    if request.method == 'POST':
        if request.FILES.get('image') == None:              # if the user didn't submit any image it is just gettin the current image that is stored in the database.
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']
            user_profile.profileimg = image 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        if request.FILES.get('image') != None:   # if the user did submit the image it will get stored in the database.
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']
            
            user_profile.profileimg = image 
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        return redirect('settings')
            
            
    return render(request,'setting.html',{'user_profile':user_profile})              # we are sending the user profile to the setting.html page itself so that it can be displayed on the page.

def signup(request):
    
    if request.method == 'POST':            # if the request is post method, then the block continues..
        username = request.POST['username']                 # taking the username from the form and storing it in a variable
        email = request.POST['email']
        password= request.POST['password']
        password2 = request.POST['password2']
        if password == password2 :
            if User.objects.filter(email = email).exists():
                messages.info(request,'Email already taken ')
                return redirect('signup')
            
            elif User.objects.filter(username = username).exists():
                    messages.info(request,'Username already taken')
                    return redirect('signup')
            else: 
                user = User.objects.create_user(username = username,email=email,password= password)
                user.save()
                
                # log in the user and redirect the user to the setting page.
                user_login = auth.authenticate(username= username, password = password)
                auth.login(request, user_login)                                                             # this was supposed automatically login the user , create a profile of the user and automatically redirect the usr to the settings page.
                
                user_model = User.objects.get(username = username)          # creating a profile object for the user
                new_profile = Profile.objects.create(user = user_model)
                new_profile.save()
                return redirect('settings')   # this was signin earlier and it was updated to setting after writing that login part while coding the setting page.
            #it should be redirected to the login page but as now we haven't done anything related to login page so we just redirect to the signup page.
        else:
            messages.info(request,'password not matching!')
            return redirect('signup')
    else:
        return render(request,'signup.html')    
        
    

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        #so we create a new variable now and try to authenticate the user.
        user = auth.authenticate(username = username , password= password)
        
        # here we are checking if the user is authenticated or not. if the user is authenticated then the user will be logged in.
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else: 
            messages.info(request,'Invalid credentials.')
            return redirect('signin')
            
    else:
        return render(request,'signin.html')


def logout(request):
    auth.logout(request)
    return redirect('signin')

def test(request):
    return HttpResponse('mew')
