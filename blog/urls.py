from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from posts.views import index, post, blog, search,post_update,post_delete,post_create

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('create/', post_create, name='post-create'),
    path('post/<int:id>/', post, name='post-detail'),
    path('post/<int:id>/update/', post_update, name='post-update'),
    path('post/<int:id>/delete/', post_delete, name='post-delete'),
    path('blog/', blog, name='blog'),
    path('search/', search, name='search'),
    path('tinymce/', include('tinymce.urls')),
]


urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
