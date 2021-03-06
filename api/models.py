from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
try:
    from localsettings import *
except ImportError:
    from Student_Org_Site_Backend.localsettings import *
if IS_PROD:
    from api.validators import *
else:
    from Student_Org_Site_Backend.api.validators import *
from django.core.exceptions import ValidationError

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Tag(models.Model):
    """
    This is a tag for user submitted post entries.
    """
    name = models.CharField(max_length=20, blank=False, unique=True, validators=[XSScheck])
    posts = models.ManyToManyField('Post', blank=True)
    def __str__(self):
        return str(self.id)+":"+self.name

    class Meta:
        verbose_name_plural = "Tags"

class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

class Orgname(models.Model):
    """
    This is static content for the org name
    """
    name = models.CharField(max_length=30, blank=False, unique=True, validators=[XSScheck])

    def __str__(self):
        return str(self.id)+":"+self.name

    class Meta:
        verbose_name_plural = "Orgnames"

class OrgnameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class Orgabout(models.Model):
    """
    This is static content for the about page
    """
    about = models.TextField(blank=False, unique=False, validators=[XSScheck])

    def __str__(self):
        return str(self.id)+":"+self.about

    class Meta:
        verbose_name_plural = "Orgabouts"

class OrgaboutAdmin(admin.ModelAdmin):
    list_display = ('id', 'about')

class Event(models.Model):
    """
    This is an event for the calendar.
    """
    title = models.CharField(max_length=20, blank=False, unique=False, validators=[XSScheck])
    start = models.CharField(max_length=40, blank=False, unique=False, validators=[XSScheck])
    end = models.CharField(max_length=40, blank=False, unique=False, validators=[XSScheck])
    #allday = models.BooleanField(unique=True)
    tags = models.ManyToManyField('tag', blank=True)
    def __str__(self):
        return str(self.id)+":"+self.title

    class Meta:
        verbose_name_plural = "Events"

class EventAdmin(admin.ModelAdmin):
    #This inner class indicates to the admin interface how to display a post
    #See the Django documentation for more information
    list_display = ('title', 'start', 'end',)

# class myUser(models.Model):
#     # '''name = models.CharField(max_length=20, blank=False, unique=True)
#     # emailAddress = models.CharField(max_length=120, blank=False, unique=True)'''
#     # profileImageUrl = models.CharField(max_length=120)
#     # posts = models.ManyToManyField('Post', blank=True)

#     user = models.OneToOneField(User)
#     profileImageUrl = models.CharField(max_length=120)
#     posts = models.ManyToManyField('Post', blank=True)

# class myUserAdmin(admin.ModelAdmin):
#     list_display = ('username',)

# class Usr(User):
#     user = models.OneToOneField(User)
#     profileImageUrl = models.CharField(max_length=120)
#     posts = models.ManyToManyField('Post', blank=True)

# class UsrAdmin(admin.ModelAdmin):
#     list_display = ('username',)

# class Usr(AbstractUser):
#     profileImageUrl = models.CharField(max_length=120)
#     posts = models.ManyToManyField('Post', blank=True)

# class UsrAdmin(admin.ModelAdmin):
#     list_display = ('username',)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profileImageUrl = models.CharField(max_length=120)
    posts = models.ManyToManyField('Post', blank=True)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user','profileImageUrl')

class Post(models.Model):
    """
    This is a forum post for storing user submitted post entries.
    """
    title = models.CharField(max_length=40, blank=False, validators=[XSScheck])
    subtitle = models.CharField(max_length=40, blank=False, validators=[XSScheck])
    image = models.CharField(max_length=120, blank=True, validators=[isImg])
    content = models.TextField(blank=False, validators=[XSScheck])
    datePublished = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField('tag', blank=True)
    def __str__(self):
        return str(self.id) +":" +self.title

    """
    def clean(self):
        if 'shit' in (self.title + self.content):
            raise ValidationError('post contains profanity')
    """
    def clean(self):
        self.title = self.title.replace('shit','****')
        self.content = self.content.replace('shit','****')

    class Meta:
        #This will be used by the admin interface
        verbose_name_plural = "Posts"

class PostAdmin(admin.ModelAdmin):
    #This inner class indicates to the admin interface how to display a post
    #See the Django documentation for more information
    list_display = ('title', 'subtitle', 'image', 'content', 'datePublished', 'author')
