from django.urls import path
from . import views
from django.contrib.auth import views as login_views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name = 'post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/update', views.PostUpdateView.as_view(), name = 'post_update'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/delete', views.PostDeleteView.as_view(), name = 'post_delete'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    # Auth urls
    path('login/', login_views.LoginView.as_view(), name='login'),
    path('logout/', login_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.register, name='registration'),
    path('ajax_search/', views.ajax_search, name='ajax_search'),
    path('help/', views.help, name='help')
]