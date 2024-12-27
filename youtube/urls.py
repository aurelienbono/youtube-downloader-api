from django.urls import path 
from . import views

urlpatterns = [
    path('download/', views.download_mp4_video_to_link, name='download_mp4_video_to_link'),

]

