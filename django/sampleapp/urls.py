from django.urls import path
from sampleapp import views

app_name = 'sample'
urlpatterns = [
    path('camera/', views.camera_view),
]