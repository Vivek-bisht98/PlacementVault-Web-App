from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('schedule/', views.schedule_list, name='schedule_list'),
    path('schedule/add/', views.schedule_add, name='schedule_add'),
    path('schedule/<int:pk>/edit/', views.schedule_edit, name='schedule_edit'),
    path('schedule/<int:pk>/delete/', views.schedule_delete, name='schedule_delete'),

    path('experience/', views.experience_list, name='experience_list'),
    path('experience/add/', views.experience_add, name='experience_add'),
    path('experience/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experience/<int:pk>/delete/', views.experience_delete, name='experience_delete'),

    path('search/', views.search_company, name='search_company'),
    path('search/roles/', views.search_roles, name='search_roles'),
    path('search/rounds/', views.search_rounds, name='search_rounds'),
    path('search/experiences/', views.search_experiences, name='search_experiences'),
]
