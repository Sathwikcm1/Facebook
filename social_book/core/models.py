from django.db import models # see here , we are importing models from db that is database.
from django.contrib.auth import get_user_model
import uuid
import datetime
# write your models here;

User = get_user_model()
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField() # what is the point of this field this is causing error so i removed it.
    bio = models.TextField(blank= True)
    profileimg = models.ImageField(upload_to='profile_images',default='blank-profile-picture.png')
    location = models.CharField(max_length=255, blank=True)#just don't randomly add the blank=True, it will cause an error.
    
    def __str__(self):                      # this is not mandatory, you can remove this if you want to., this is related to our admin panel, this will show up.
        return self.user.username
    
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)    # this is the id for each post of the user or many users., this is the primary key, this must be entered in the form. so we give a default to this one. that is uuid.uuid4
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')   #this will create a folder inside the directory media called post_images and all the images are stored in there.
    caption = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    no_of_likes = models.IntegerField(default = 0)              #because when user uploads the image the likes should be zero by default.
    def __str__(self):
        return self.user

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    username= models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
class followersCount(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user