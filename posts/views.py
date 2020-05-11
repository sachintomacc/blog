from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render,get_object_or_404,redirect,reverse
from posts.models import Post,Author,PostView
from .forms import CommentForm,PostForm
from marketing.models import SignUp


def get_category_count():
    queryset = Post.objects.values(
        'categories__title').annotate(Count('categories'))
    return queryset


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None 


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    if request.method == 'POST':
        email = request.POST['email']
        new_signup = SignUp()
        new_signup.email = email
        new_signup.save()
    context = {'posts': featured, 'latest': latest}
    return render(request, 'index.html', context)


def post(request, id):
    post = get_object_or_404(Post,id=id)
    post_view = PostView.objects.get_or_create(post=post,user=request.user)
    # print(post_view)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    category_count = get_category_count()
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse('post-detail',kwargs={'id':post.id} ))
    context = { 'post' : post , 'form': form ,'most_recent' : most_recent, 'category_count': category_count}
    return render(request, 'post.html',context)

    #  path('post/<int:id>/', post, name='post-detail'),


def blog(request):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    query_set = Post.objects.all()
    page_request_var = 'page'
    paginator = Paginator(query_set, 2)
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    # print(category_count)

    context = {'post_list': paginated_queryset,
               'page_request_var': page_request_var,
               'most_recent': most_recent, 'category_count': category_count}
    return render(request, 'blog.html', context)


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    # print(queryset)
    context = {'queryset': queryset}
    return render(request, 'search_results.html', context)

def post_update(request,id):
    post = get_object_or_404(Post,id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance=post )
    if form.is_valid():
        form.instance.author = get_author(request.user)
        form.save()
        return redirect(reverse('post-detail',kwargs={'id':form.instance.id}))
    context = {'form':form, 'title' : 'Update'}
    return render(request,'post_create.html',context)

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect(reverse('blog'))

def post_create(request):
    form = PostForm(request.POST or None,request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = get_author(request.user,)
            form.save()
            return redirect(reverse('post-detail', kwargs={'id': form.instance.id }))
    context = { 'form': form , 'title' : 'Create'}
    return render(request,'post_create.html',context)

