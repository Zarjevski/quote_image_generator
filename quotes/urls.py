from django.urls import path
from .views import upload_quotes, success, failed

urlpatterns = [
    path('upload/', upload_quotes, name='upload_quotes'),
    path('success/', success, name='success'),
    path('failed/', failed, name='failed'),  # Add this line

]
