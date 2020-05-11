from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField

User = get_user_model()


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class PostView(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    



class Post(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    categories = models.ManyToManyField(Category)
    content = HTMLField(null=True, blank=True)
    featured = models.BooleanField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    # view_count = models.IntegerField(default=0)
    thumbnail = models.ImageField()
    previous_post = models.ForeignKey('self',related_name='previous' , on_delete = models.SET_NULL,null=True,blank=True)
    next_post = models.ForeignKey('self', related_name='next', on_delete = models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse("post-update", kwargs={"id": self.id})
    
    def get_delete_url(self):
        return reverse("post-delete", kwargs={"id": self.id})
    
    @property
    def comments(self):
        return self.comments.all()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()




class Comment(models.Model):
    comment = models.TextField()
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
    