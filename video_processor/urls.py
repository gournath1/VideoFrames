from django.urls import path
from .views import VideoProcessAPIView, test_api_view

urlpatterns = [
   path('process-video/', VideoProcessAPIView.as_view(), name='process-video'),
   path('test-api/', test_api_view, name='test-api'),
]
