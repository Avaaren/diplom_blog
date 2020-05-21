from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.core.serializers import serialize
from pytils.translit import slugify

from .models import Post
from .forms import (
    CommentForm, 
    SearchForm, 
    LoginForm, 
    UserForm,
    PostForm   
    )

from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count

from django.views.generic import CreateView, UpdateView, DeleteView


def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag,})

# Create your views here.


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, status='published',
                             publish__year=year, publish__month=month, publish__day=day
                             )
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:5] 
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts,
                                                     }
                  )

def register(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registration/register_done.html', {'user_form': user_form})
    else:
        user_form = UserForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

def ajax_search(request):
    data = {}
    search_value = request.GET.get('value')
    print(search_value)
    result_queryset = Post.objects.filter(title__icontains=search_value).only('title')
    title_list = [str(x) for x in result_queryset]
    links_list = [str(x.get_absolute_url()) for x in result_queryset]
    print(links_list)
    data['search_result'] = title_list
    data['links'] = links_list
    return JsonResponse(data)


class PostCreateView(CreateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/create.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.slug = slugify(instance.title)
        instance.save()
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post/update.html'
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user != self.object.author:
            return redirect(reverse('blog:post_list'))
        else:
            return super().get(request, *args, **kwargs)

    def get_object(self):
        slug = self.kwargs.get('post')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')

        return get_object_or_404(Post,
                                 slug=slug, created__year=year,
                                 created__month=month, created__day=day)

class PostDeleteView(DeleteView):
    
    model = Post
    template_name = 'blog/post/delete.html'

    def get_object(self):
        slug = self.kwargs.get('post')
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        day = self.kwargs.get('day')
        post = get_object_or_404(Post,
                                 slug=slug, created__year=year,
                                 created__month=month, created__day=day)
        if post.author != self.request.user:
            return redirect(reverse('blog:post_list'))
        else:
            return post
       

    def get_success_url(self):
        return reverse('blog:post_list')

                                 