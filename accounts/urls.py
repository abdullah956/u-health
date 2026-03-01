from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('create-account/', views.create_account, name='create_account'),
    path('logout/', views.logout_view, name='logout'),
]
