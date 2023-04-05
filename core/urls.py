from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import UserCreateAPIView, LoginView, RefreshTokenView


urlpatterns = [

    ### Home
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)