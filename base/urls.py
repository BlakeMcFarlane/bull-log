from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('save_course/', views.saveCourse, name='save_course'),
    path('my_classes/', views.trackedClasses, name='tracked_classes')
]