from django.contrib import admin
from posts.models import Post, Category, Author,Comment
from marketing.models import SignUp
# Register your models here.

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(SignUp)
admin.site.register(Comment)
