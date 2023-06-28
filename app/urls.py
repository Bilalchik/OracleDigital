from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('auth/', views.authentication_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('student-list/', views.StudentListView.as_view(), name='student_list'),
    path('student-delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('student-detail/<int:pk>/', views.student_detail, name='student_detail'),
    path('student-add/', views.student_add, name='student_add'),
    path('send_message', views.send_message, name='send_message')
]
