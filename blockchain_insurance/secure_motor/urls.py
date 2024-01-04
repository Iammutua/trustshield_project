from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('policies/', views.policies, name='policies'),
    path('fileclaim/', views.fileclaim, name='fileclaim'),
    path('myclaims/', views.myclaims, name='myclaims'),
    path('support/', views.support, name='support'),
    path('logout/', views.logout, name='logout'),
    path('applyPolicy/', views.applyPolicy, name='applyPolicy'),
    path('terms/', views.terms, name='terms')
]